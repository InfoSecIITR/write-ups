# Recipe Archival Workshop

## DESCRIPTION

New interns in the Recipe Archival Workshop have a simple task- upload images of yummy delicacies and dream about tasting them some day.

## SOLUTION

In this challenge we are given a file upload webpage where we can upload files of type `png`, `jpg`, `jpeg`, etc. My initial approach was to look for a file upload vulnerability but the issue was we don't know where the file is stored on the server, so even if we do get our script on the server, we don't have a way to execute. 

We see that the webpage doesn't allow certain filetypes so all we can do now is to see if there are some other filetypes that are allowed. So, I fired up Burp Suite and send the upload request to intruder and ran a Sniper attack with this wordlist [File-Extensions-Wordlist.txt](https://raw.githubusercontent.com/InfoSecWarrior/Offensive-Payloads/main/File-Extensions-Wordlist.txt).

This gives us the flag at the `.tiff` extension.

Flag: `VishwaCTF{today_i_wanted_to_eat_a_croissant_QUASO}`