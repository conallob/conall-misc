#!/bin/bash
# vim:ts=2:sw=2:expandtab:ft=sh:fileencoding=utf-8

# $Id$

# Copyright (c) 2013, Conall O'Brien
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the <organization> nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY Conall O'Brien ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <copyright holder> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# author: Conall O'Brien (conall@conall.net)

INPUT=$1
OUTPUT=$2
AUDIO_TRACK=${3:-1}
AUDIO_CODEC=${4:-ac3}
OUTPUT_DIR="/Users/Shared/DVDRips"

# caffeinate (to add a power management assertion)
/usr/bin/caffeinate /Applications/HandBrakeCLI \
  --main-feature -i "${INPUT}" \
  -e x264 -a ${AUDIO_TRACK} -E copy:${AUDIO_CODEC} \
  -o "$OUTPUT_DIR/${OUTPUT}.mkv" -m
