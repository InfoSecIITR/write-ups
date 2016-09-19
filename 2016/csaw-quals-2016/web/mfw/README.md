# Web 125 - MFW

> Writeup by f0xtr0t (Jay Bosamiya)

A quick look at the website's `.git` folder shows that we can access files such as `.git/HEAD` etc, but the directory wasn't directly browsable or clonable, so by using [dumper from GitTools](https://github.com/internetwache/GitTools). Looking through the repo and the files, the `flag.php` file doesn't have the flag, and no history information that has the file. Hence, I thought I should look at the source, and figure out a flaw that can be used on the server.

I was kinda stuck for a while, until @captn3m0 (Nemo) told me that the asserts (in [index.php](git-folder/index.php)) were in strings. Obviously, there was some sort of eval being done on the string.

So, using the page string as `' and die(show_source('templates/flag.php')) or '`, the assert would cause the source of the `flag.php` file to be revealed, which it did :)

BTW, the URL to run that page was `http://web.chal.csaw.io:8000/?page=%27%20and%20die(show_source(%27templates/flag.php%27))%20or%20%27`

Fun challenge overall :) Goes on to show that one should NEVER let user input be `eval`d in any way. [This stackoverflow answer](https://stackoverflow.com/questions/3115559/exploitable-php-functions) has a nice list of all the executable pathways in PHP.
