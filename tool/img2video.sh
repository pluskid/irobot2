#!/bin/bash

ffmpeg -r 50 -b 8000k -i capture/%04d.png battle.swf
