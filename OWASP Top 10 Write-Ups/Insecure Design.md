# Try Hack Me - Compiled
**OWASP Category: A06:2025 – Insecure Design** 

Analyzing a binary file, we discovered the function logic of the program and, therefore, were able to determine the password.

## Tools:
- **Ghira**
- **Gdb**
- **checksec**

## Methodology:

1. **Executing the binary**
    - After executing the binary in the command line, a prompt to input a password showed up. After putting in a random password, the program gave us a status: Try again!.

    <img src="\assets\Compiled_execute.png" alt="execute_program" width="1000px">

2. **Gathering more info about the file**
    - Using cmd tools 'file' and 'checksec', I found out:
    1. The binary is not stripped - some strings are human-readable
    2. No canary - buffer overflow is possible
    3. PIE enabled - addresses of functions differ after each execution

    <img src="\assets\Compiled_fileinfo.png" alt="file_info" width="1000px">
    ¨
    - With 'gdp' tool, I can see what functions does the file have. I want to focus on the main function to analyze it further.

    <img src="\assets\Compiled_functions.png" alt="functions" width="1000px">

3. **Analyzing the file with Ghira**
    - I analyzed the file in Ghira and was able to see the decompiled C code of function 'main'.

    ```c
    undefined8 main(void)

    {
    int iVar1;
    char local_28 [32];
  
    fwrite("Password: ",1,10,stdout);
    __isoc99_scanf("DoYouEven%sCTF",local_28);
    iVar1 = strcmp(local_28,"__dso_handle");
    if ((-1 < iVar1) && (iVar1 = strcmp(local_28,"__dso_handle"), iVar1 < 1)) {
    printf("Try again!");
    return 0;
    }
    iVar1 = strcmp(local_28,"_init");
    if (iVar1 == 0) {
    printf("Correct!");
    }
    else {
    printf("Try again!");
    }
    return 0;
    ```

    - The functions does these steps:
    1. "__isoc99_scanf("DoYouEven%sCTF", local_28);" -> Password needs to start with "DoYouEven", then there is some input from local_28.
    2. "iVar1 = strcmp(local_28, "_init");" -> local_28 is comapred to the string "_init". 
    3. "if (iVar1 == 0) {printf("Correct!");}" -> if _init = local28, the program prints "Correct!"

4. **Trying the password**
    - I tried to input password: DoYouEven_init. The password was correct.

    <img src="\assets\Compiled_Correct.png" alt="correct_password" width="1000px">

## Remediation
Do not embed passwords inside the client-side binary.