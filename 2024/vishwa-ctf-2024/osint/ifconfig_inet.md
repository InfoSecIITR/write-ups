# OSINT/ ifconfig_inet:
## DESCRIPTION

In the labyrinth of binary shadows, Elliot finds himself standing at the crossroads of justice and chaos. Mr. Robot, the enigmatic leader of the clandestine hacktivist group, has just unleashed a digital storm upon Evil Corp's fortress. The chaos is palpable, but this is just the beginning.

As the digital tempest rages, Elliot receives a cryptic message from Mr. Robot. "To bring down Evil Corp, we must cast the shadows of guilt upon Terry Colby," the message echoes in the encrypted channels. However, in the haze of hacktivism, Elliot loses the crucial IP address and the elusive name of the DAT file, leaving him in a digital conundrum.

To navigate this cybernetic maze, Elliot must embark on a quest through the binary underbelly of Evil Corp's servers. The servers, guarded by firewalls and encrypted gatekeepers, conceal the secrets needed to ensure Terry Colby's fall.

Guide Elliot to the his destiny.

Flag Format : VishwaCTF{name of DAT file with extension_IP address of Terry Colby}

E.g : VishwaCTF{file.dat_0.0.0.0}

## Solution

For this challenge we were supposed to find a file and an ip address 

So we just needed to search on google the  terry colby ip address

Then for .dat file we have to dig further and spend some time and finally 

we land on this reddit post

https://www.reddit.com/r/MrRobot/comments/bcpe4u/why_would_a_dat_file_fsociety00dat_from_the_first/

From there we get the .dat file and so is the flag😊

VishwaCTF{fsociety00.dat_218.108.149.373}