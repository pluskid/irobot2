import sys
from   os            import makedirs
from   os            import path
from   random        import randint
import pygame
from   pygame.locals import *
from   pygame.sprite import Group

from   .sprite    import SpRobot, SpAnimation, SpShoot
from   .engine    import Engine
from   .event     import EvBorn, EvDeath, EvIdle
from   .exception import ConfigError
from   .robot     import Robot
from   .util      import vec2d

class God(object):
    def __init__(self, config):
        self._config = config
        self._robots = dict()
        self._engine = Engine(self._config['engine'])

        self._gp_robots = Group()
        self._gp_animations = Group()
        self._gp_shoots = Group()
        self._engine.add_group(self._gp_robots)
        self._engine.add_group(self._gp_animations)
        self._engine.add_group(self._gp_shoots)

        if self._config['system']['capture']:
            self._frames = []

        self._teams = {}

        # TEST CODE
        from irobot2.action.path_to import find_path
        self._path = find_path(self._engine.map, vec2d(100, 100), vec2d(500, 500))

    def build_robot(self, rtype, team, name):
        robot_id = '%s.%s' % (team, name)
        if self._robots.has_key(robot_id):
            raise ConfigError('Robot %s already exists'%robot_id)
        try:
            config = self._config['setting']['robots'][rtype]
        except KeyError:
            raise ConfigError('No such robot type: %s'%rtype)
        rpropos = {
                'k.type': rtype,
                'k.god': self,
                'k.alpha': 0,
                'k.direction': vec2d(1, 0),
                'k.team': team,
                'k.name': name,
                'k.speed': config['speed'],
                'k.angle_speed': config['angle_speed'],
                'k.strike': config['strike'],
                'k.defend': config['defend'],
                'k.sight': config['sight'],
                'k.hp': config['hp'],
                'k.cp': config['cp']
                }
        robot = Robot(rpropos)
        sprite = SpRobot(robot, self._engine.get_image(config['image']))
        robot['k.sprite'] = sprite
        self._gp_robots.add(sprite)
        self._robots[robot_id] = robot

        self._teams.setdefault(team, [])
        self._teams[team].append(name)
        return robot

    def add_animation(self, animation):
        self._gp_animations.add(animation)

    def create_shoot(self, position, direction, sprobot, stype, strike):
        sconfig = self._config['setting']['shoots'][stype]
        image = self._engine.get_image(sconfig['image'])
        sprite = SpShoot(image, sprobot, position, direction, 
                         sconfig, strike)
        self._gp_shoots.add(sprite)

    def create_explosion(self, position, target, damage):
        self.create_explosion_animation(position, 'explode-small')
        target.hurt(damage, self)

    def create_explosion_animation(self, position, exp_type):
        images = self._engine.get_images(exp_type)
        explode = SpAnimation(position, images)
        self._gp_animations.add(explode)

    def robot_look_around(self, robot):
        rect = Rect(0, 0, robot['k.sight'], robot['k.sight'])
        rect.center = robot['k.position']
        spritecollide = rect.colliderect
        sprite = robot['k.sprite']
        targets = []
        for s in self._gp_robots:
            if s != sprite and spritecollide(s.rect):
                targets.append(s)
        return targets

    def put_robots(self):
        # currently we only support two teams, robots are 
        # put on the top right and bottom left cornors
        if len(self._teams) != 2:
            raise ConfigError('Only two teams supported in this version')
        teams = self._teams.keys()
        geo = self._engine.map.geometry
        start_pos = [(geo[0]-1, 0), (0, geo[1]-1)]
        xinc = [-1, 1]
        for i in (0, 1):
            team = teams[i]
            pos = start_pos[i]
            for rbname in self._teams[team]:
                robot = self._robots['%s.%s' % (team, rbname)]
                robot['k.position'] = \
                        self._engine.map.tile2pixel(pos, center=True)
                robot['k.alpha'] = 255
                pos = (pos[0]+xinc[i], pos[1])

    def collision_detect(self, rect, objs):
        spritecollide = rect.colliderect
        def cd_group(grps):
            for grp in grps:
                for s in grp:
                    if (not s in objs) and spritecollide(s.rect):
                        return s
            return None
        return cd_group((self._gp_robots, 
                         self._engine.map.obstacles))

    @property
    def game_map(self):
        return self._engine.map

    @property
    def config(self):
        return self._config

    @property
    def engine(self):
        return self._engine

    def start(self):
        self._engine.render(self._path)   # initial render to init graphics
        self.put_robots()

        for robot in self._robots.itervalues():
            self.robot_born(robot)

        capture = self._config['system']['capture']
        paused = False
        while True:
            terminate = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate = True
                    break
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        terminate = True
                        break
                    elif event.key == K_SPACE:
                        paused = not paused
            if terminate:
                break

            time_passed = self._engine.tick()
            if paused:
                continue

            for shoot in self._gp_shoots:
                shoot.step(self, time_passed)

            # TODO: terminate the game when all
            # robot of one team is dead
            all_dead = True
            for robot in self._robots.itervalues():
                if robot['k.alive'] == True:
                    all_dead = False
                    self.perform_action(robot, time_passed)

                if all_dead:
                    break
            self._engine.render(self._path)


            if capture:
                self._frames.append(self._engine.screen.copy())
        if capture:
            self.save_capture()
        sys.exit()

    def robot_born(self, robot):
        robot['k.alive'] = True
        robot.event(EvBorn())
        robot.start()
    def robot_die(self, robot):
        robot['k.alive'] = False
        robot.event(EvDeath())
        
    def perform_action(self, robot, time_passed):
        action = robot['k.action']
        if action is not None:
            event = action.update(self, time_passed)
            if event is not None:
                robot['k.action'] = None
                robot.event(event)
        else:
            robot.event(EvIdle())

    def save_capture(self):
        dest_dir = self._config['system']['capture_output']
        if not path.exists(dest_dir):
            makedirs(dest_dir)

        nframes = len(self._frames)
        print 'Saving %d frames...' % nframes
        for i in range(nframes):
            if (i+1) % 20 == 0:
                sys.stdout.write('.')
                sys.stdout.flush()
                if (i+1) % 1000 == 0:
                    sys.stdout.write('\n')
            fn = path.join(dest_dir, '%04d.png'%(i+1))
            pygame.image.save(self._frames[i], fn)
        sys.stdout.write('\nDone\n')
