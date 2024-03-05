# YourBonus
## Description 
I am very kind, and you're my friend too. I was about to share some flags with you, but unfortunately, a ransomware attack occurred on the file containing those flags. All the flags got encrypted by the ransomware. After cross-checking the directories, I found the ransomware file and some other related items. I'm going to share that information with you. However, due to the ransomware, I'm unable to provide you with the flags 😥😥. Now, I need your help to recover those flags. Can you assist me, please? Your cooperation would be highly appreciated, and you will receive a reward for your help.

Note : Ransomware are not meant to be executed as it can harm your systems (although this won't)

### Files
[ransomeware.exe](ransomeware.exe)
[READMe.txt](README.txt)
[your_hackday_data0.txt](Your_hacked_data0.txt)

### Writeup
- Analysed the `ransomeware.exe` in IDA (a powerful debugging tool). It has functions like `zarathos`, `lucifer`, `ghost_ridders`, `matter_manipulation`, `trigon` and few more.
- Functioning of binary: It takes a file as Input, i.e., `Flags.txt`, reads its content, perform some operations and stores the result in `your_hacked_data0.txt`
- `zarathos` : This function takes the string and gets the substring (random number of characters from the beginning) from the string, reverses it and then reverses the last remaining part and after it, reverses the whole string. For example: String : `VishwaCTF{Sl4y3r}`  1. `4lS}FTCawhsiVy3r}` 2. `4lS}FTCawhsiV}r3y` 3. `y3r}VishwaCTF{Sl4`
- `lucifer` : string[i] = chr(ord(string[i])-2)) (here 2 can be other number also, like 1)
- In this binary, characters from `0 to 9` are mapped with special symbols like `@#$!`
- Mapping is as follows :
  ```
  0:* 1:)
  2:$ 3:@
  4:^ 5:#
  6:( 7:!
  8:% 9:&
  
  ```
- Characters of the resultant string after `zarathos` & `lucifer` are converted into ascii codes and then mapped accordingly.
- Thus, the logic behind the encoding is decoded.
- To get the flag, reverse the operations on the data given in `your_hackded_data0.txt`
``` python
str='''%##^!)@#(!!(!$%)%&%#(!^&%#^(#*##^&^%&)&)%^!)%)!*($($%$(#(%%&%#@^@)^%!)!)((&@##&$###^^*&@##@@^&#^&@@%####!$!@!@(#!)&)%#%&!$#^@^^%!*%)&)&@@((@!@@@(%!@(@(@!^%)%&!!%#!!%###($@^
((!^#!%#()^&#)&@#*%*^&&@(^^&(@(%%@!^%&#(@&&)&)(%^(!&%^!)%)!*%#(@(#%$(%%&%*#*!(#)&$@^(%!^(!#%^&&@%#@(#)#*%@%$^(^(%###(%%@!^%&#(@&&)&)!(%$((#*%^!)%)!*(%%&(((%%#!(#)^(()^&##^%%##*%*#*#*%!#)&@#*%*
!@((!!!(@&@%@&##!$((!#^&###^!#()#%(*(!##^&!$!)%#%@((((%#%&%@!*!)(@!(&@#(&)%&#(#!&)%##^#^($!)#^@^!)!@!#%##*%*^&#)&@(^^&(@%@%$!)(%%@!^#&()&@(*%&#(@&&)&)%^!)%)!*%#(@(#%$(%%&#%&@#*%*^&&@%*#*!(#)^(
%)((%^@&!(!(%^(^%@%&#####*#^&)@%^*@^@(&)##^&^*@(@@@&()(*#%(*!!!!%#!)^&#((@!)!$((@&@%%)!@%#@&^&#^^%#^#@#@()(*#%#(!)%)^*@(@@^%&)%&&)(%%#((%&&)%^!)%)!*(#%$(%%&####^%#^^*@(#^^&%@%#!(((@%
(*()()%&#&&@!!(((%^%@#@@#)!@(!%*!!%)!#(!!!(%!%%#&)!)!!%$&@%$!*!)!((&%)&@#*(@%*!@!@%#^*@((*(*%!!*&@&@%!%#@^@#%&&)^(#@%!%#(!!(@%^((&@^@#%!%#(!%^&@@#%!%#@&@@@#%!@)%&@@%!@^&$%@%#%*!*%$(^&)%#@#
'''
str= str.replace('%','8').replace('(','6').replace('#','5').replace('^','4').replace('@','3').replace('$','2').replace(')','1').replace('*','0').replace('&','9').replace('!','7')

```
- This gives the data having ascii codes.
``` python
str=[85,54,71,35,67,76,72,81,89,85,67,49,85,46,50,55,.........,89,33,87,34,92,83,85,80,70,82,64,91,85,35]
res=''
for i in range(len(str)):
    res += chr(str[i]+2)
print(res)
```
- The result is: 
```
W8I%ENJS[WE3W04932]]VISH@@TCF[W$!2IID_9^98*_9#38_(99JKKCI]W[J8$2HS]_&AK#FKAALS[OWOW9@$DL;W?35_4R3_B3AFUL[:)]]F0QVISHWACTF[R4N5^$FLE<3_W&54UT00W9FUL[:)]]NTD4VISHF[DFWN50?392W4R44Y5_4RKDON)()9JDM398M?<>E93JIWUDDW[UHIAN_:][:;]W88@I8$IKMW4R35_B3AUTIFUL=?_>[:)]]VISHWACTF[<_4R3_R4N50SDV)NNVBU[9948](*$&]93*&#)?><>OOWI3:AIJD)(SKW)382877?><:IS*&#2][]FWD[]VISHCTF[9928*&83UWND(>??[=_ODF2%#5KEROSMEOFPW]IOT_THINGS_4ARKKW*&>>YH__YW$%[]07YWEN(0G$%YWEV_%YW)#%Y![#Y$^UWRHTB]W%
```
#### Flag is `VISHWACTF[4R3_R4N50MW4R35_B3AUTIFUL]`


  
