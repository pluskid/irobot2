=============
Game Settings
=============

Attack damage
=============

When robot `A` use shooting `S` to strike robot `B`, the damage of `B`
is calculated as::

  A.strike * S.damage * (1-B.defend)

`damage` of shooting is a absolute value, `strike` of a robot is a
scale factor and `defend` of a robot should be with range `[0, 1]`.
