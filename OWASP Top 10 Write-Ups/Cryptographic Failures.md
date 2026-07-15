# Try Hack Me - Crypto Failures

**OWASP Category: A04:2025 Cryptographic Failures** 

A public-facing .bak file was found containing php script that is used to generate authentication cookies, after reviewing the mechanism of the script I found a way to create a new cookie that was successfully used as admin authentication cookie.

## Tools:
- **NMap**
- **GoBuster**

## Methodology:

1. **Enumerating open ports with nmap**
    - Nmap scan: nmap -sVC 10.112.191.122 
    -Results showed open ports **80** and **22**.

    <img src="\assets\Crypto_Failures.png" alt="nmap_reuslts" width="1000px">

2. **Exploring port 80**
    - This is what the website looks like on port 80:

    <img src="\assets\Crypto_Failures_80.png" alt="port_80" width="1000px">

    - There is an interesting comment left in the source code of the website signifying there could be some public-facing backup files:

    ```html
    <!-- TODO remember to remove .bak files-->
    ```

3. **Enumerating directories with .bak extension**
    - I user **gobuster** to enumerate directories that have php files ending with the extension .bak.
    
    ```bash
    gobuster dir -u http://10.112.191.122 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php.bak
    ```

    - We have found this public-facing path: /index.php.bak:

    <img src="\assets\Crypto_Failure_dir.png" alt="direcotries" width="1000px">

    - I visited the URL path and a file **index.php.bak** was downloaded.

    <img src="\assets\Crypto_Failures_file.png" alt="file_download" width="1000px">

4. **Analyzing the .bak file**
    - The file index.php.bak contains a script for generating cookies.

    1. The script is loading a secret key ($ENC_SECRET_KEY) from config.php file.
    2. A function generates 2-digits salt: $SALT = generatesalt(2);
    3. A string ($secure_cookie_string) is created from 3 items: user:user-agent:secret-key (for example: guest:Mozilla/5.0:SuperSecretKey)
    4. The function make_secure_cookie() transforms the string into the value of the cookie.
    5. The script then sets 2 separate cookies:
        secure_cookie=result made by function make_secure_cookie()
        user=user (guest/admin)
    6. The secure cookie string is separated into blocks of 8 symbols and function cryptstring() hashes each string with the value of the salt.

    ```php
    <?php
    include('config.php');

    function generate_cookie($user,$ENC_SECRET_KEY) {
    $SALT=generatesalt(2);
    
    $secure_cookie_string = $user.":".$_SERVER['HTTP_USER_AGENT'].":".$ENC_SECRET_KEY;

    $secure_cookie = make_secure_cookie($secure_cookie_string,$SALT);

    setcookie("secure_cookie",$secure_cookie,time()+3600,'/','',false); 
    setcookie("user","$user",time()+3600,'/','',false);
    }

    function cryptstring($what,$SALT){

    return crypt($what,$SALT);

    }

    function make_secure_cookie($text,$SALT) {

    $secure_cookie='';

    foreach ( str_split($text,8) as $el ) {
    $secure_cookie .= cryptstring($el,$SALT);
    }

    return($secure_cookie);
    }

    function generatesalt($n) {
    $randomString='';
    $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    for ($i = 0; $i < $n; $i++) {
    $index = rand(0, strlen($characters) - 1);
    $randomString .= $characters[$index];
    }
    return $randomString;
    }

    function verify_cookie($ENC_SECRET_KEY){


    $crypted_cookie=$_COOKIE['secure_cookie'];
    $user=$_COOKIE['user'];
    $string=$user.":".$_SERVER['HTTP_USER_AGENT'].":".$ENC_SECRET_KEY;

    $salt=substr($_COOKIE['secure_cookie'],0,2);

    if(make_secure_cookie($string,$salt)===$crypted_cookie) {
        return true;
    } else {
        return false;
    }
    }

    if ( isset($_COOKIE['secure_cookie']) && isset($_COOKIE['user']))  {

    $user=$_COOKIE['user'];

    if (verify_cookie($ENC_SECRET_KEY)) {
        
    if ($user === "admin") {
   
        echo 'congrats: ******flag here******. Now I want the key.';

            } else {
        
        $length=strlen($_SERVER['HTTP_USER_AGENT']);
        print "<p>You are logged in as " . $user . ":" . str_repeat("*", $length) . "\n";
	    print "<p>SSO cookie is protected with traditional military grade en<b>crypt</b>ion\n";    
    }

    } else { 

    print "<p>You are not logged in\n";

    }

    }
    else {

    generate_cookie('guest',$ENC_SECRET_KEY);
    
    header('Location: /');

    }
    ?>
    ```

5. **Get the value of our cookie**
    - From Inspect we copy the value of our cookie.

    <img src="\assets\Crypto_Failures_cookie.png" alt="cookie" width="1000px">

6. **Reversing the cookie script**
    - The cookie is composed of 29 strings each composed of 13 symbols:

    lb7NSQVKII/xMlbSWUALKQkTdclbqNHCHlMb2IglbVqJC01B.ixolbB7iJhmQibUUlb04yZjAU6tbolbUs7NJp6wQkIlbkhj828r0JCclbyFRIEvG3Ik2lb/8Tt1C2AM.6lblaFxGrwRKMMlbph0SXuMCedklbjfONPBmXZSIlbjh4lifLVPY.lbFlQbRJviwKolbd9gbgcYvhQglb77NNFoZAUBklb7JS3G1oOhQIlbN/BsekmCM0olbkQb.FfO/DBolbGQ1M.CnpZYQlbt49SHHVbIp2lbctBi8ETlzjIlbLXG3tP9wJA2lbUfn3Z7bPyc6lb6hhaY67E6/glb0UPWjIZpfw2lbnXRE.VVii1Mlb0pXLxIYnSs

    - We need to alter only the first part - change the user:guest to user:admin.

    - Salt = lb
    - UserAgent = Mozilla/5.0 (X11; Linux x86_64; rv:152.0) Gecko/20100101 Firefox/152.0
    - User = admin

    ```bash
    php -r 'echo crypt("admin:Mo","1b"), PHP_EOL;'
    ```

7. **Authenticating as admin with a forged cookie**
    - I put the new cookie into Inspect->Storage->Cookies and also changed the other cookies to user: admin. After reloading the page we got the flag.

    <img src="\assets\Crypto_Failures_flag.png" alt="flag" width="1000px">


## Remediation

Replace the cookie-generating mechanism with a cryptographic authentication mechanism such as HMAC-SHA256. Do not use control values from the client such as the User Agent of the client.

