This is basically my notes document, used while reverse-engineering the BASIC and splitting it into manageable chunks.

## Program Listing (Spectrum BASIC)

```basic
  10 REM ISLAND OF SECRETS -- requires at least a 48K machine
```
Because heaven forbid you'd have anything less.

### Main Program
Begins by setting the game speed (I think) and calling the initialisation subroutine
```basic
  15 LET wv=70
  20 GO SUB 2820
```
#### Main program loop
```basic
  30 LET d=r: IF r=20 THEN LET d=FN r(80)
  40 GO SUB 650: CLS : PRINT "ISLAND OF SECRETS", "TIME REMAINING:";  l
  50 PRINT g$;  TAB (0);  "STRENGTH = ";  INT (y);  TAB (18);  "WISDOM = ";  x: PRINT g$
  55 LET li=VAL (a$(1))
  60 PRINT "YOU ARE ";  (i$(li))( TO h(li));  " "; : GO SUB 720: LET n=0
  70 FOR i=1 TO c4
  80 LET c=0: READ y$
  90 IF l(i)=r AND f(i)<1 THEN LET c=1
 100 IF n>0 AND c=1 THEN LET a$=a$+","
 110 IF c=1 THEN LET a$=a$+" "+y$: LET n=n+1
 120 NEXT i
 130 IF n>0 THEN LET a$="*YOU SEE"+a$: GO SUB 720
 140 PRINT : PRINT g$;  f$
 150 PRINT : PRINT "WHAT WILL YOU DO"; 
 160 INPUT e$: PRINT "  ";  e$
 ```
The next bit handles the user input. `e$` contains the full text typed, and this gets split into `c$` and `x$` for first word, rest of sentence respectively. `li` is set to the length of `e$`. We then go through `v$`, set on line `4340`, in order to change the verb into its verb index (see list of verbs below.) We then `GO SUB 760` which does exactly the same, but for the second word (why it needs a subroutine, I don't know.) So, by the end of this code block, `a` is the id of the verb, `o` is the id of the noun, the timer `l` gets decreased by 1, and `b$` gets set to a string of numbers indicating the overall state. This comprises of the numerical ID of the object last specified, the location of that object, the state (array `f`) of that object and the numerical ID of the current location.
```basic 
 170 LET c$="": LET x$="": LET a=0: LET o=52: LET li=LEN (e$)
 180 FOR i=1 TO li-1
 190 IF e$(i)=" "AND c$=""THEN LET c$=e$( TO i-1)
 200 IF e$(i+1)<>" "AND c$>""THEN LET x$=e$(i+1 TO ): LET i=li-1
 210 NEXT i
 220 IF x$=""THEN LET c$=e$
 230 IF LEN (c$)<3 THEN LET c$=c$+"???"
 240 FOR i=1 TO v
 250 IF c$( TO 3)=v$(3*(i-1)+1 TO 3*(i-1)+3) THEN LET a=i
 260 NEXT i
 270 GO SUB 760
 280 LET b$="": IF a=0 THEN LET a=v+1
 290 IF x$="???"THEN LET f$="MOST ACTIONS NEED TWO WORDS"
 300 IF a>v OR o=52 THEN LET f$=w$+c$+" "+x$
 310 IF a>v AND o=52 THEN LET f$="WHAT!"
 320 LET l=l-1: LET y=FN s(z)
 330 LET b$=STR$(o)+STR$(l(o))+STR$(f(o))+STR$(r)
 ```
The next line calls a subroutine based on the first word (verb) typed.
```basic 
 340 GO SUB g(a)
```
The next code block is a load of special case conditions.
```basic  
 350 IF r=61 THEN LET x=x-FN r(2)+1
 360 IF r=14 AND FN r(3)=1 THEN LET y=y-1: LET f$="YOU ARE BITTEN"
 370 IF f(36)<1 AND -r<>f(22) THEN LET f(36)=f(36)+1: LET l(36)=r: LET y=y-1
 380 IF r<>l(16) AND l(16)>0 THEN LET l(16)=1+FN r(4)
 390 IF r<>l(39) THEN LET l(39)=10*(FN r(5)-1)+7+FN r(3)
 400 IF r=l(39) AND r<>l(43) AND f(13)>-1 THEN LET y=y-2: LET x=x-2
 410 IF r<78 THEN LET l(32)=76+FN r(2)
 420 IF r=33 OR r=57 OR r=73 AND FN r(2)=1 THEN LET l(25)=r
 430 IF r=l(32) AND FN r(2)=1 AND f(32)=0 THEN GO SUB 1310
 440 IF r=19 AND y<70 AND f(43)=0 AND FN r(4)=1 THEN LET f$="PUSHED INTO THE PIT": LET f(w)=1
 450 IF r<>l(41) THEN LET l(41)=21+(FN r(3)*10)+FN r(2)
 460 IF r=l(41) THEN LET f(41)=f(41)-1: IF f(41)<-4 THEN GO SUB 1230
 470 IF f(43)=0 THEN LET l(43)=r
 480 IF l(43)<18 AND r<>9 AND r<>10 AND f(w-2)<1 THEN GO SUB 1330
 490 IF r=18 THEN LET y=y-1
 500 IF y<50 THEN LET o=FN r(9): GO SUB 1530: IF l(o)=r THEN LET f$="YOU DROP SOMETHING"
 510 IF l<900 AND r=23 AND f(36)>0 AND FN r(3)=3 THEN GO SUB 1360
 520 IF r=47 AND f(8)>0 THEN LET f$=f$+" YOU CAN GO NO FURTHER"
 530 IF f(8)+f(11)+f(13)=-3 THEN LET f(w)=1: GO SUB 2800
 540 IF f(w)=0 AND l>0 AND y>1 AND x>1 THEN GO TO 30
```

350. If the player is in "A livid growth of mad orchids", then reduce the wisdom by 2 or 3
360. If the player is in "A thicket of biting bushes", then 33% chance of reducing strength by 1
370. If the storm's variable is <1 and the location ID isn't the negative of the wine's variable, then increase the storm's variable by 1, move the storm to the current location and reduce strength by 1
380. If the player isn't with the canyon beast and the canyon beast's location isn't 0 then move the canyon beast to either the "Depths of the Mutant Forest", "A Path Out of the Overgrown Depths", "A Carnivorous Tree" or "A Corral Beneath the Crimson Canyon" (equal chance of each)
390. If the player isn't with Omegan, move him somewhere randomly
400. If the player *is* with Omegan, but not with Median, and the coal's variable is higher than -1, then reduce strength and wisdom by 2 each
410. If the player isn't in the Swampman's lair, move the Swampman to either the swamp or the stump village
420. If the player is on the log pier, on the Island of Secrets or the river's edge by the bridge, 50% chance the Boatman will appear
430. If the player is with the Swampman, and his variable is 0, 50% chance of calling the Swampman subroutine at line `1310`
440. If the player is on the edge of the well with strength lower than 70 and Median's variable is 0, 25% chance of being pushed into the well (ending the game)
450. If the player isn't with the logmen, move them randomly
460. If the player *is* with the logmen, reduce their variable by 1, and if it's lower than -4, call the Logmen subroutine at line `1230`
470. If Median's variable is 0, move him to where the player is
480. If Median is in a certain location and you're not, then it calls the extra hint subroutine at `1330`
490. If you're in the clone storage area, reduce strength by one
500. If your strength is under 50 then pick one of the first nine objects and call the drop routine. If it's successful, change the message to "You dropped something" to alert the player.
510. If time is under 900 and you're on the leafy path (start area), and the storm's variable is over 0, then there's a 1/3 chance the Storm subroutine will be called.
520. If you're by the two clashing stones and the pebble's variable is over 0 then add "you can go no further" to the status message
530. If the sum of the pebble, staff and coal's variables is -3 then call the "You won!" subroutine
540. If the game isn't over, and your location is valid, and your strength and wisdom are over 1, then repeat the main loop.
#### Game Over
If line `540` doesn't return to the beginning of the main loop, then the game is over.
```basic 
 550 IF l<1 OR y<1 THEN LET f$="YOU HAVE FAILED, THE EVIL ONE SUCCEEDS"
 560 PRINT : PRINT f$: PRINT "YOUR FINAL SCORE=";  INT (x+y+(ABS (l/7*(l<640))))
 570 PRINT : PRINT : PRINT "GAME OVER"
 580 STOP 
```

Seems to be just a dummy return. I doubt this line will ever be run. Possibly from line `340` if we run out of values in the array `g`.
```basic
 640 RETURN 
```

### Get Location Data
This is called from line `40`. Before being called, `d` is set to the number of the room, or a random value between 1 and 80 if the current room is `20` (the room of secret visions). The subroutine stores the name of the room in `a$` and a string representing which way the player can move in `d$`. The string in `d$` is four numbers for north, south, east, west respectively, and a 1 means a wall, and 0 means passable. If the location is `20` (secret visions) the only exit is west, and if the location is `39` ("here") the exits are randomised.
```basic
 650 LET d=d*10+lr : REM 1>=d>=80
 660 RESTORE d : REM anything from 2870 to 3660 ie the location strings
 670 READ a$
 680 LET d$=a$(LEN(a$)-3 TO ): LET a$=a$( TO LEN(a$)-4)
 690 IF r=39 THEN LET rd=FN r(5): LET d$="101110100"(rd TO rd+3)
 700 IF r=20 THEN LET d$="1110"
 710 GO SUB 2780: RETURN 

```

### Pretty printing routine
Seems to be just a way of displaying the contents of `a$` letter by letter.
```basic
 720 FOR i=2 TO LEN (a$): LET e$=a$(i)
 730 PRINT e$; : IF e$=" "AND PEEK (23688)<z THEN PRINT 
 740 NEXT i
 750 PRINT ". "; : LET a$="": RETURN 

```


```basic
 760 IF LEN (x$)<3 THEN LET x$=x$+"???"
 770 FOR i=1 TO w
 780 IF x$( TO 3)=z$(3*(i-1)+1 TO 3*(i-1)+3) THEN LET o=i
 790 NEXT i: IF o=0 THEN LET o=52
 800 RETURN 

```

### Move subroutine
```basic
 810 LET d=0: LET c=0: IF o=52 THEN LET d=a
 820 IF o>c4 AND o<w THEN LET d=o-c4
 830 IF b$="500012"OR b$="500053"OR b$="500045"THEN LET d=4
 840 IF b$="500070"OR b$="500037"OR b$="510011"OR b$="510041"THEN LET d=1
 850 IF b$="510043"OR b$="490066"OR b$="490051"THEN LET d=1
 860 IF b$="510060"OR b$="480056"THEN LET d=2
 870 IF b$="510044"OR b$="510052"THEN LET d=3
 880 IF b$="490051"AND f(29)=0 THEN GO SUB 2110: RETURN 
 890 IF r=l(39) AND (x+y<180 OR r=10) THEN LET f$=w$+"LEAVE!": RETURN 
 900 IF r=l(32) AND f(32)<1 AND d=3 THEN LET f$="HE WILL NOT LET YOU PAST": RETURN 
 910 IF r=47 AND f(44)=0 THEN LET f$="THE ROCKS MOVE TO PREVENT YOU": RETURN 
 920 IF r=28 AND f(7)<>1 THEN LET f$="THE ARMS HOLD YOU FAST": RETURN 
 930 IF r=45 AND f(40)=0 AND d=4 THEN LET f$="HISSSS!": RETURN 
 940 IF r=25 AND f(16)+l(16)<>-1 AND d=3 THEN LET f$="TOO STEEP TO CLIMB": RETURN 
 950 IF r=51 AND d=3 THEN LET f$="THE DOOR IS BARRED!": RETURN 
 955 IF d=5 THEN GO TO 970
 960 IF d>0 THEN IF d$(d)="0"THEN LET r=r+VAL ("-10+10+01-01"(d*3-2 TO d*3)): LET c=1
 970 LET f$="OK"
 980 IF d<1 OR c=0 THEN LET f$=w$+"GO THAT WAY"
 990 IF r=33 AND l(16)=0 THEN LET l(16)=FN r(4): LET f(16)=0: LET f$="THE BEAST RUNS AWAY!"
1000 IF r<>l(25) OR o<>25 THEN RETURN 
1010 LET f$="": LET a$="#YOU BOARD THE CRAFT "
1020 IF x<60 THEN LET a$=a$+s$
1030 LET a$=a$+t$
1040 GO SUB 2740: FOR d=1 TO wv*2: NEXT d
1050 IF x<60 THEN LET a$="#TO SERVE OMEGAN FOREVER!": LET f(w)=1
1060 IF x>59 THEN LET a$="#THE BOAT SKIMS THE DARK SILENT WATERS": LET r=57
1070 GO SUB 2750: FOR d=1 TO wv*2: NEXT d: RETURN 

```

### Get, Take, Pick, Catch subroutine
```basic
1080 IF ((f(o)>0 AND f(o)<9) OR l(o)<>r) AND o<=c3 THEN LET f$="WHAT "+x$+"?": RETURN 
1090 IF b$="3450050"THEN LET y=y-8: LET x=x-5: LET f$="THEY ARE CURSED": RETURN 
1100 IF b$="3810010"THEN GO SUB 1370
1110 IF (a=15 AND o<>20 AND o<>1) OR (a=29 AND o<>16) OR o>c3 THEN LET f$=w$+c$+" "+x$: RETURN 
1120 IF l(o)=r AND (f(o)<1 OR f(o)=9) AND o<c3 THEN LET l(o)=0: LET a=-1
1130 IF o=16 AND l(10)<>0 THEN LET l(o)=r: LET f$="IT ESCAPED": LET a=0
1140 IF o>c1 AND o<c2 THEN LET f=f+2: LET a=-1
1150 IF o>=c2 AND o<=c3 THEN LET g=g+2: LET a=-1
1160 IF o>c1 AND o<c3 THEN LET l(o)=-81
1170 IF a=-1 THEN LET f$="TAKEN": LET x=x+4: LET e=e+1: IF f(o)>1 THEN LET f(o)=0
1180 IF b$<>"246046"OR l(11)=0 THEN RETURN 
1190 LET f$=u$: LET l(o)=r: IF FN r(3)<3 THEN RETURN 
1200 LET a$="#"+u$+r$
1210 LET r=63+FN r(6): LET l(16)=1: LET f$=""
1220 GO SUB 2740: RETURN 

```

### Logmen subroutine
This is called from the main loop. Every time you're in the same location as the logmen, `f(41)` gets decreased. If it reaches `-4` then this subroutine is called. You're moved to either the water or the storeroom, and, if you're carrying flowers or the jug, they are moved to the cabin.
```basic
1230 CLS : LET f$="": LET a$="#THE LOGMEN "+m$
1240 LET f(41)=0: LET y=y-4: LET x=x-4
1250 IF r<34 THEN LET a$=a$+"THROW YOU IN THE WATER": LET r=32
1260 IF r>33 THEN LET a$=a$+"TIE YOU UP IN A STOREROOM": LET r=51
1270 GO SUB 2750: FOR d=1 TO wv: NEXT d
1280 FOR i=3 TO 4
1290 IF l(i)=0 THEN LET l(i)=42
1300 NEXT i: RETURN 

```

### Swampman subroutine
This is called randomly from the main loop (line `430`) if you are in the same location as the Swampman.
```basic
1310 LET a$="*THE SWAMPMAN TELLS HIS TALE"
1320 GO SUB 2740: LET f(32)=-1: RETURN 

```

This is called from the main loop under certain circumstances.
```basic
1330 LET f$="MEDIAN CAN DISABLE THE EQUIPMENT"
1340 IF l(8)=0 THEN LET f$=f$+" AND ASKS YOU FOR THE PEBBLE YOU CARRY"
1350 RETURN 

```

Also called from the main loop in certain circumstances.
```basic
1360 LET f(36)=-(FN r(4)+6): LET f$="A STORM BREAKS OVERHEAD!": RETURN 

```

Called from the get subroutine in certain circumstances.
```basic
1370 FOR k=1 TO 30: CLS : PRINT "////LIGHTNING FLASHES!": NEXT k
1380 LET l(39)=r: LET y=y-8: LET x=x-2: RETURN 

```

### Give subroutine
```basic
1390 IF (o<>24 AND l(o)>0) OR o=52 THEN LET f$="YOU DON'T HAVE THE "+x$: RETURN 
1400 PRINT "GIVE THE "; x$; " TO WHOM"; : INPUT x$
1410 LET q=o: GO SUB 760: LET n=o: LET o=q
1420 IF r<>l(n) THEN LET f$="THE "+x$+" IS NOT HERE": RETURN 
1430 IF b$="10045"AND n=40 THEN LET l(o)=81: LET f(40)=1: LET f$="THE SNAKE UNCURLS"
1440 IF b$="2413075"AND n=30 AND g>1 THEN LET f(11)=0: LET f$="HE OFFERS HIS STAFF": LET g=g-1
1450 LET b$=b$( TO 3): LET f$="IT IS REFUSED"
1460 IF b$="300"AND n=42 THEN LET x=x+10: LET l(o)=81
1470 IF b$="120"AND n=42 THEN LET x=x+10: LET l(o)=81
1480 IF b$="40-"AND n=32 THEN LET f(n)=1: LET l(o)=81
1490 IF b$( TO 2)="80"AND n=43 THEN LET l(o)=81: GO SUB 1560
1500 IF l(o)=81 OR (o=24 AND l(11)>0 AND g>0) THEN LET f$="IT IS ACCEPTED"
1510 IF n=41 THEN LET l(o)=51: LET f$="IT IS TAKEN"
1520 RETURN 

```

### Drop, leave subroutine
If 'drop' is entered, the subroutine is called from line `1530`. If 'leave' is entered, the subroutine is called from `1540`, removing the chance that the item might be broken.
```basic
1530 IF o=4 AND l(o)=0 THEN LET l(o)=81: LET x=x-1: LET f$="IT BREAKS!": RETURN 
1540 IF l(o)=0 AND o<=c1 THEN LET l(o)=r: LET f$="DONE": LET e=e-1
1550 RETURN 
```

Called from the give routine in certain circumstances.
```basic
1560 LET a$="*HE TAKES IT ": IF r<>8 THEN LET a$=a$+"RUNS DOWN THE CORRIDOR,"
1570 GO SUB 2740: LET a$="*AND CASTS IT INTO THE CHEMICAL VATS, PURIFYING THEM WITH"
1580 LET a$=a$+" A CLEAR BLUE LIGHT REACHING FAR INTO THE LAKES AND RIVERS BEYOND"
1590 LET f(8)=-1: GO SUB 2750: FOR d=1 TO wv*2: NEXT d: RETURN 

```


```basic
1600 IF l(i)<>0 AND i<c1 THEN LET i=i+1: GO TO 1600
1610 IF l(i)=0 THEN LET l(i)=r: LET f(i)=0: GO SUB 1540: LET f$="YOU DROP SOMETHING"
1620 RETURN 

```

### Eat subroutine
```basic
1630 IF (o<c1 OR o>c3) AND x$<>"???"THEN LET f$=w$+c$+" "+x$: LET x=x-1: RETURN 
1640 LET f$="YOU HAVE NO FOOD": IF f>0 THEN LET f=f-1: LET y=y+10: LET f$="OK"
1650 IF o=3 THEN LET x=x-5: LET y=y-2: LET f$="THEY MAKE YOU VERY ILL!"
1660 RETURN 

```

### Drink subroutine
```basic
1670 IF o=31 THEN GO SUB 2380: RETURN 
1680 IF x$<>"???"AND (o<21 OR o>c3) THEN LET f$=w$+c$+" "+x$: LET x=x-1: RETURN 
1690 LET f$="YOU HAVE NO DRINK": IF g>0 THEN LET g=g-1: LET y=y+7: LET f$="OK"
1700 RETURN 

```

### Ride subroutine
```basic
1710 IF b$( TO 4)="1600"THEN LET f(o)=-1: LET f$="IT ALLOWS YOU TO RIDE"
1720 RETURN 

```

### Open subroutine
```basic
1730 IF b$="2644044"THEN LET f$="CHEST OPEN": LET f(6)=9: LET f(5)=9: LET f(15)=9
1740 IF b$="2951151"THEN LET f$="THE TRAPDOOR CREAKS": LET f(29)=0: LET x=x+3
1750 RETURN 

```

### Chop, chip, tap, break subroutine
```basic
1760 LET y=y-2: IF b$="3577077"AND l(9)=0 THEN LET f(23)=0: LET l(23)=r
1770 IF v>15 AND v<19 AND (l(9)=0 OR l(15)=0) THEN LET f$="OK"
1780 IF b$="1258158"OR b$="2758158"AND l(15)=0 THEN LET f(12)=0: LET f(27)=0: LET f$="CRACK!"
1790 IF b$( TO 4)="1100"AND r=10 THEN GO SUB 1980
1800 IF a=18 AND (o>29 AND o<34) OR (o>38 AND o<44) OR o=16 THEN GO SUB 1900
1810 RETURN 

```

### Fight, strike, attack, hit subroutine
```basic
1820 LET y=y-2: LET x=x-2: IF r<>l(o) AND l(o)<>0 THEN RETURN 
1830 IF o=39 THEN LET f$="HE LAUGHS DANGEROUSLY"
1840 IF o=32 THEN LET f$="THE SWAMPMAN IS UNMOVED"
1850 IF o=33 THEN LET f$=w$+"TOUCH HER!": LET l(3)=81
1860 IF o=41 THEN LET f$="THEY THINK THAT'S FUNNY!"
1870 IF r=46 THEN GO SUB 1200
1880 IF b$( TO 4)="1400"AND r=l(39) THEN GO SUB 1980
1890 LET y=y-8: LET x=x-5: RETURN 

```

### Kill subroutine
Normally called from `1910`. Called from the break subroutine from `1900`
```basic
1900 IF l(9)>0 THEN RETURN 
1910 LET y=y-12: LET x=x-10: LET f$="THAT WOULD BE UNWISE!"
1920 IF r<>l(o) THEN RETURN 
1930 LET f(w)=1: LET a$="#A THUNDER SPLITS THE SKY!": LET f$=""
1940 LET a$=a$+"IT IS THE TRIUMPHANT VOICE OF OMEGAN.": GO SUB 2740
1950 LET a$="#WELL DONE ALPHAN! THE MEANS BECOME THE END.."
1960 LET a$=a$+"I CLAIM YOU AS MY OWN! HA HA HAH!": GO SUB 2750
1970 FOR d=1 TO wv: NEXT d: LET x=0: LET l=0: LET y=0: RETURN 

```

Called from the break and fight subroutines. If the object is 11 (the staff) then we call `2010`. If the object is greater than 11 then we call `2060`
```basic
1980 CLS : GO SUB 2010*((o-10)=1)+2060*((o-10)>1)
1990 LET x=x+10: LET l(o)=81: LET f(o)=-1: GO SUB 720: FOR d=1 TO wv*2: NEXT d
2000 RETURN 

```

### Break staff subroutine
```basic
2010 LET a$="#IT SHATTERS RELEASING A DAZZLING RAINBOW OF COLOURS!"
2020 IF l(2)<>r THEN RETURN 
2030 LET a$=a$+"THE EGG HATCHES INTO A BABY DAKTYL "+o$
2040 LET l(39)=81: LET l(2)=81: LET f(2)=-1: LET y=y+40
2050 RETURN 

```

### Break something else routine
```basic
2060 IF l(13)<>r THEN RETURN 
2070 LET a$="*THE COAL BURNS WITH A WARM RED FLAME": LET f(13)=-1
2080 IF r=10 AND r=l(39) THEN LET a$=a$+" WHICH DISSOLVES OMEGAN'S CLOAK": LET y=y+20
2090 RETURN 

```

### Swimming subroutine
```basic
2100 IF r<>51 OR f(29)>0 THEN LET f$=w$+c$+" HERE": LET x=x+1
2110 LET x=x-1: LET r=FN r(5): CLS : PRINT "SWIMMING IN THE POISONOUS WATERS"
2120 LET j=0: LET b$="": LET f$="YOU SURFACE": PRINT "YOUR STRENGTH = ";  INT (y)
2130 FOR i=1 TO r
2140 IF y<15 THEN PRINT "YOU ARE VERY WEAK"
2150 PRINT "WHICH WAY "; : INPUT x$: PRINT x$: LET x$=x$(1): LET b$=b$+x$: NEXT i
2160 FOR i=1 TO r
2170 LET y=FN s(z)-3: IF b$(i)="N"THEN LET j=j+1
2180 NEXT i: IF r/2>j AND y>1 THEN GO TO 2110
2190 IF y<2 THEN LET f$="YOU GOT LOST AND DROWNED"
2200 LET r=30+FN r(3): RETURN 

```

### Shelter subroutine
```basic
2210 IF f(36)>-1 THEN RETURN 
2220 CLS : PRINT "YOU CAN RUN TO SHELTER IN:": PRINT "1) GRANDPA'S SHACK"
2230 PRINT "2) CAVE OF SNELM": PRINT "3) LOG CABIN": PRINT "CHOOSE FROM 1-3": INPUT a$
2240 IF a$>"0"AND a$<"4"THEN LET r=CODE ("A >"(VAL (a$)))-21: LET f(22)=-r
2250 PRINT "YOU RUN BLINDLY THROUGH THE STORM": LET f$="YOU REACH SHELTER"
2260 FOR d=1 TO wv: NEXT d: RETURN 

```

### Help, scratch subroutine
```basic
2270 IF b$="3075075"OR b$="3371071"THEN LET f$="HOW WILL YOU DO THAT"
2280 IF b$="3371071"AND a=28 THEN LET f(3)=0: LET f$="SHE NODS SLOWLY": LET x=x+5
2290 RETURN 

```

### Read, examine subroutine
```basic
2300 LET f$="EXAMINE THE BOOK FOR CLUES"
2310 IF b$( TO 3)="600"THEN LET f$=l$
2320 RETURN 

```

### Fill subroutine
```basic
2330 IF b$="40041"THEN LET f(4)=-1: LET f$="FILLED"
2340 RETURN 

```

### Say subroutine
```basic
2350 LET f$=x$: IF x$=h$ AND r=47 AND f(8)=0 THEN LET f(44)=1: LET f$=j$
2360 IF x$<>p$ OR r<>l(42) OR l(3)<81 OR l(12)<81 THEN RETURN 
2370 LET f$="HE EATS THE FLOWERS - AND CHANGES": LET f(42)=1: LET f(43)=0: RETURN 

```

### Wait, rest subroutine
Called from `2400` normally. Only called from `2380` from the drink subroutine, if you try to drink the liquor.
```basic
2380 IF f(4)+l(4)<>-1 THEN LET f$="YOU DON'T HAVE "+x$: RETURN 
2390 CLS : PRINT "YOU TASTE A DROP AND..": FOR d=1 TO wv: NEXT d: LET f$="*OUCH!": LET y=y-4: LET x=x-7
2400 CLS : FOR i=1 TO ABS (f(36))+3
2410 LET l=l-1: IF y<100 OR -r=f(22) THEN LET y=y+1
2420 PRINT "TIME PASSES": FOR d=1 TO wv: NEXT d
2430 NEXT i
2440 IF l>100 OR f(36)<1 THEN LET x=x+2: LET f(36)=1
2450 IF a=37 OR a=36 THEN LET f$="OK"
2460 RETURN 

```

### Wave subroutine
```basic
2470 IF r=l(25) THEN LET f$="THE BOATMAN WAVES BACK"
2480 IF b$( TO 3)="700"THEN LET f(7)=1: LET f$=n$: LET x=x+8
2490 RETURN 

```

### Rub, polish subroutine
```basic
2500 LET f$="A-DUB-DUB": IF b$( TO 4)<>"2815"THEN RETURN 
2510 IF f(o)=1 THEN LET f(o)=0: LET f$=k$: RETURN 
2520 IF l(5)=0 THEN LET f(8)=0: GO SUB 1080: LET f$="THE STONE UTTERS "+h$
2530 RETURN 

```

### Info subroutine
```basic
2540 CLS : PRINT " INFO - ITEMS CARRIED": GO SUB 2780
2550 PRINT g$;  TAB (0);  " FOOD="; f; TAB (23); "DRINK="; g: PRINT g$; : LET f$="OK"
2560 FOR i=1 TO c4
2570 READ y$: IF l(i)=0 THEN PRINT y$
2580 NEXT i
2590 PRINT g$; : GO SUB 2730: RETURN 

```

### Load / save subroutine
```basic
2600 LET c$="LOAD": IF a=41 THEN LET c$="SAVE"
2610 PRINT "PREPARE TO "; c$: GO SUB 2730
2640 IF a=41 THEN LET f(50)=r: LET f(49)=y: LET f(48)=x: LET f(47)=f: LET f(46)=g: LET f(45)=l
2660 IF a=40 THEN LOAD "ISDATA"DATA l(): LOAD "ISDATA"DATA f()
2670 IF a=41 THEN SAVE "ISDATA"DATA l(): SAVE "ISDATA"DATA f()
2700 IF a=40 THEN LET r=f(50): LET y=f(49): LET x=f(48): LET f=f(47): LET g=f(46): LET l=f(45)
2710 LET f$="OK": RETURN 

```

### Quit subroutine
```basic
2720 LET f(w)=-1: LET f$="YOU RELINQUISH YOUR QUEST.": LET l=1: RETURN 

```

### Press a key subroutine
Called from the info and load/save subroutines. Waits for user input before continuing.
```basic
2730 INPUT "PRESS RETURN";  a$: RETURN 

```

### Display message routine
Clears the screen, calls the routine that prints a string letter by letter, waits, and then returns.
```basic
2740 CLS 
2750 GO SUB 720: FOR d=1 TO wv: NEXT d: RETURN 
```

### Reset the reading of data
Effectively calls `RESTORE 3760`
```basic
2780 RESTORE lr+810
2790 RETURN 
```

### You win!
```basic
2800 LET a$="*THE WORLD LIVES WITH NEW HOPE!": GO SUB 2750
2810 LET f$="YOUR QUEST IS OVER": RETURN 
```

### Initialisation

```basic
2820 PRINT "INITIALISING"
2830 LET lr=2860: LET z=8
2840 LET v=42: LET w=51: LET c4=43
2850 DIM i$(7,7)
2860 DIM l(52): DIM f(52): DIM h(7): DIM g(43)
```

```basic
2870 DATA "4THE FURTHEST DEPTHS OF THE FOREST1001"
2880 DATA "4THE DEPTHS OF THE MUTANT FOREST1000"
2890 DATA "7A PATH OUT OF THE OVERGROWN DEPTHS1000"
2900 DATA "6A CARNIVOROUS TREE1000"
2910 DATA "4A CORRAL BENEATH THE CRIMSON CANYON1110"
2920 DATA "7THE TOP OF A STEEP CLIFF1011"
2930 DATA "4THE MARSH FACTORY1001"
2940 DATA "4THE SLUDGE FERMENTATION VATS1110"
2950 DATA "7THE UPPERMOST BATTLEMENTS1001"
2960 DATA "4OMEGAN'S SANCTUM1110"
2970 DATA "4SNELM'S LAIR0001"
2980 DATA "2A DARK CAVE0000"
2990 DATA "1BROKEN BRANCHES0100"
3000 DATA "1A THICKET OF BITING BUSHES0000"
3010 DATA "1A HUGE GLASS STONE1110"
3020 DATA "7THE EDGE OF CRIMSON CANYON0011"
3030 DATA "4THE CLONE FACTORY0101"
3040 DATA "4A CORRIDOR OF CLONE STORAGE CASKS1100"
3050 DATA "7EDGE OF THE WELL0000"
3060 DATA "4THE ROOM OF SECRET VISIONS1110"
3070 DATA "4SNELM'S INNER CHAMBER0111"
3080 DATA "3THE SOUTHERN EDGE OF THE FOREST0101"
3090 DATA "7A LEAFY PATH1000"
3100 DATA "3A FORK IN THE PATH0100"
3110 DATA "7AN APPARENTLY UNCLIMBABLE ROCKY PATH1100"
3120 DATA "7A LEDGE ATOP THE CRIMSON CANYON0010"
3130 DATA "4A TALL ENTRANCE CHAMBER1101"
3140 DATA "4A LOW PASSAGE WITH ARMS REACHING FROM THE WALLS1010"
3150 DATA "7THE APPROACH TO THE WELL OF DESPAIR0001"
3160 DATA "4A DIM CORRIDOR DEEP IN THE CASTLE1010"
3170 DATA "4THE STAGNANT WATERS OF THE CRAWLING CREEK1001"
3180 DATA "4A SHALLOW POOL OFF THE CREEK1100"
3190 DATA "7A LOG PIER, JUTTING OUT OVER THE CREEK0000"
3200 DATA "4A STRETCH OF FEATURELESS DUNES1100"
3210 DATA "1A GROUP OF TALL TREES1010"
3220 DATA "7A NARROW LEDGE AT THE SUMMIT OF THE CANYON0011"
3230 DATA "2A MONSTEROUS PORTAL IN THE CASTLE WALL0011"
3240 DATA "4A CHAMBER INCHES DEEP WITH DUST0001"
3250 DATA "4HERE1111"
3260 DATA "2A CARVED ARCHWAY0010"
3270 DATA "4A SMALL HUT IN THE LOG SETTLEMENT0111"
3280 DATA "1A HUGE SPLIT-LOG TABLE1001"
3290 DATA "4THE PORCH OF THE LOGMEN'S CABIN0110"
3300 DATA "4GRANDPA'S SHACK1101"
3310 DATA "3A CLEARING IN THE TREES BY A RICKETY SHACK0010"
3320 DATA "4THE NEST OF A HUGE DACTYL0111"
3330 DATA "6THE CASTLE OF DARK SECRETS BY TWO HUGE STONES0011"
3340 DATA "4A ROOM LITTERED WITH BONES0111"
3350 DATA "4THE CELL OF WHISPERED SECRETS0111"
3360 DATA "4THE LIBRARY OF WRITTEN SECRETS0111"
3370 DATA "4A REFUSE STREWN STOREROOM1111"
3380 DATA "4THE LOGMEN'S HALL0000"
3390 DATA "5A LOG BUILDING1000"
3400 DATA "7A RUTTED HILLSIDE1100"
3410 DATA "7A WINDSWEPT PLAIN AMONGST STONE MEGALITHS0100"
3420 DATA "7THE STEPS OF AN ANCIENT PYRAMID1010"
3430 DATA "7THE ISLAND OF SECRETS0111"
3440 DATA "1A BROKEN MARBLE COLUMN1001"
3450 DATA "7AN EXPANSE OF CRACKED, BAKED EARTH1100"
3460 DATA "4A DESERTED ADOBE HUT1010"
3470 DATA "4A LIVID GROWTH OF MAD ORCHIDS1011"
3480 DATA "4A CORNER STREWN WITH BROKEN CHAIRS0111"
3490 DATA "7THE BRIDGE NEAR TO A LOG SETTLEMENT0011"
3500 DATA "1A CRUMBLING MASS OF PETRIFIED TREES1011"
3510 DATA "3THE EDGE OF THE PYRAMID1101"
3520 DATA "7THE ROOF OF THE ANCIENT PYRAMID0100"
3530 DATA "3AN IMPASSABLE SPLIT IN THE PYRAMID1110"
3540 DATA "7A BARREN BLASTED WASTELAND0001"
3550 DATA "4AN EXPANSE OF BLEAK, BURNT LAND1100"
3560 DATA "5A DELAPIDATED ADOBE HUT0110"
3570 DATA "4THE HEART OF THE LILIES0101"
3580 DATA "4THE MIDST OF THE LILIES1100"
3590 DATA "3A RIVER'S EDGE BY A LOG BRIDGE0100"
3600 DATA "3A PETRIFIED VILLAGE BY A RIVER CROWDED WITH LILIES0100"
3610 DATA "4THE REMAINS OF A VILLAGE1100"
3620 DATA "3THE ENTRANCE TO A PETRIFIED VILLAGE1100"
3630 DATA "4A SWAMP MATTED WITH FIBROUS ROOTS1100"
3640 DATA "2A VILLAGE OF HOLLOW STUMPS DEFYING THE SWAMP0100"
3650 DATA "4A TUNNEL INTO ONE OF THE TREE STUMPS1100"
3660 DATA "4A HOLLOW CHAMBER MANY METRES IN DIAMETER1110"
```

```basic
3670 DATA "A SHINY APPLE"
3680 DATA "A FOSSILISED EGG"
3690 DATA "A LILY FLOWER"
3700 DATA "AN EARTHENWARE JUG"
3710 DATA "A DIRTY OLD RAG"
3720 DATA "A RAGGED PARCHMENT"
3730 DATA "A FLICKERING TORCH"
3740 DATA "A GLISTENING PEBBLE"
3750 DATA "A WOODMAN'S AXE"
3760 DATA "A COIL OF ROPE"
3770 DATA "A RUGGED STAFF"
3780 DATA "A CHIP OF MARBLE"
3790 DATA "A POLISHED COAL"
3800 DATA "A PIECE OF FLINT"
3810 DATA "A GEOLOGIST'S HAMMER"
3820 DATA "A WILD CANYON BEAST"
3830 DATA "A GRAIN LOAF"
3840 DATA "A JUICY MELON"
3850 DATA "SOME BISCUITS"
3860 DATA "A GROWTH OF MUSHROOMS"
3870 DATA "A BOTTLE OF WATER"
3880 DATA "A FLAGON OF WINE"
3890 DATA "A FLOWING SAP"
3900 DATA "A SPARKLING FRESHWATER SPRING"
3910 DATA "THE BOATMAN"
3920 DATA "A STRAPPED OAK CHEST"
3930 DATA "A FRACTURE IN THE COLUMN"
3940 DATA "A MOUTH-LIKE OPENING"
3950 DATA "AN OPEN TRAPDOOR"
3960 DATA "A PARCHED, DESSICATED VILLAGER"
3970 DATA "A STILL OF BUBBLING GREEN LIQOUR"
3980 DATA "A TOUGH SKINNED SWAMPMAN"
3990 DATA "THE SAGE OF THE LILIES"
4000 DATA "WALL AFTER WALL OF EVIL BOOKS"
4010 DATA "A NUMBER OF SOFTER ROOTS"
4020 DATA "FIERCE LIVING STORM THAT FOLLOWS YOU"
4030 DATA "MALEVOLENT WRAITHS WHO PUSH YOU TOWARD THE WELL"
4040 DATA "HIS DREADED CLOAK OF ENTROPY"
4050 DATA "OMEGAN THE EVIL ONE"
4060 DATA "AN IMMENSE SNAKE WOUND AROUND THE HUT"
4070 DATA "A GROUP OF AGGRESSIVE LOGMEN"
4080 DATA "THE ANCIENT SCAVENGER", "MEDIAN"
```

Resets the data read pointer to the start of the item data
```basic
4090 GO SUB 2780
```

The following is read into `i$` at some point, prepositions to be put on the front of location descriptions.
```basic
4100 DATA "BY", "FACING", "AT", "IN", "OUTSIDE", "BENEATH", "ON"
```

The lengths (in characters) of each of the above, used to avoid printing extra spaces because the Spectrum's arrays were pretty static in terms of memory mapping
```basic
4105 DATA 2,6,2,2,7,7,2
```

The following defines some constants and some initial variable values. It also stores some constant strings which are defined here presumably so it's not so easy when typing in the program to work out how to win the game.
```basic
4110 RESTORE lr+1230: REM 2860+1230 = 4090
4120 FOR i=1 TO 7: READ i$(i): NEXT i
4125 FOR i=1 TO 7: READ h(i): NEXT i
4130 LET r=23: LET b=8: LET l=1000: LET e=0
4140 LET c1=16: LET c2=21: LET c3=24: LET f=2: LET g=2
4150 LET f=2: LET g=2
4160 LET y=100: LET x=35
4170 LET h$="MNgIL5;/U^kZpcL%LJ\5LJm-ALZ/SkIngRm73**MJFF          "
4180 LET q$="90101191001109109000901000111000000100000010000000000"
4190 LET g$="--------------------------------"
4200 LET f$="LET YOUR QUEST BEGIN"
4210 LET k$="REFLECTIONS STIR WITHIN"
4220 LET l$="REMEMBER ALADDIN IT WORKED FOR HIM"
4230 LET m$="DECIDE TO HAVE A LITTLE FUN AND "
4240 LET n$="THE TORCH BRIGHTENS"
4250 LET u$="YOU ANGER THE BIRD"
4260 LET w$="YOU CAN'T "
4270 LET p$="REMEMBER OLD TIMES"
4280 LET r$=" WHICH FLIES YOU TO A REMOTE PLACE"
4290 LET s$="FALLING UNDER THE SPELL OF THE BOATMAN "
4310 LET t$="AND ARE TAKEN TO THE ISLAND OF SECRETS"
4320 LET j$="THE STONES ARE FIXED"
4330 LET o$="WHICH TAKES OMEGAN IN ITS CLAWS AND FLIES AWAY"
```

This is a single string containing a list of verbs the parser recognises. It only checks the first three characters, which is probably why save and load are `XSAVE` and `XLOAD`.
```basic
4340 LET v$="N??S??E??W??GO?GETTAKGIVDROLEAEATDRIRIDOPEPICCHOCHITAPBREFIGSTRATT"
4350 LET v$=v$+"HITKILSWISHEHELSCRCATRUBPOLREAEXAFILSAYWAIRESWAVINFXLOXSAQUI"
```

This is the same idea, but nouns rather than verbs.
```basic
4360 LET z$="APPEGGFLOJUGRAGPARTORPEBAXEROPSTACHICOAFLIHAMCANLOAMELBISMUS"
4370 LET z$=z$+"BOTWINSAPWATBOACHECOLSTOTRAVILLIQSWASAGBOOROOASAWRACLOOMESNA"
4380 LET z$=z$+"LOGSCAMEDNORSOUEASWESUP?DOWIN?OUT???"
```

decodes some obfuscated text.
```basic
4390 FOR i=1 TO w+1
4400 LET l(i)=CODE (h$(i))-32: LET f(i)=CODE (q$(i))-48
4410 NEXT i
4420 LET h$="STONY WORDS"
4430 DEF FN r(z)=INT (RND*z+1)
4440 FOR i=1 TO 43: READ g(i): NEXT i
4450 DEF FN s(z)=y-(e/c4+.1)
4460 RETURN 

```

the next bit appears to be a bunch of line numbers to `GO SUB` to. Line `340` seems to be the only place this happens. I feel that in modern programming this would be a `case` statement.

Interestingly, line `640` is just a `RETURN` statement.

```basic
4470 DATA 810,810,810,810,810,1080,1080,1390,1530
4480 DATA 1540,1630,1670,1710,1730,1080,1760,1760,1760,1760
4490 DATA 1820,1820,1820,1820,1910,2100,2210,2270,2270,1080
4500 DATA 2500,2500,2300,2300,2330,2350,2400,2400,2470,2540
4510 DATA 2600,2600,2720,640

```

-----

## Variables

Scalars

| Variable | Initial value | Purpose        |
| -------- | ------------- | -------------- |
| r        | 23            | location id    |
| l        | 1000          | time remaining |
| y        | 100           | strength       |
| x        | 35            | wisdom         |

Strings


| Variable | Initial value                      | Purpose                                                                         |
| -------- | ---------------------------------- | ------------------------------------------------------------------------------- |
| f$       | LET YOUR QUEST BEGIN               | The information text to print at the top of the page when asking for user input |
| h$       | Item locations, then `STONY WORDS` |                                                                                 |


Arrays

| Variable | Size | Contains                                        |
| -------- | ---- | ----------------------------------------------- |
| l        | 52   | one per noun, stores the object's location id   |
| f        | 52   | one per noun ...flag?                           |
| g        | 43   | the subroutine data from lines `4470` to `4510` |
| i$       | 7, 7 | prepositions                                    |
| h        | 7    | lengths of the seven prepositions               |

Constants

| Name | Value | Description                               |
| ---- | ----- | ----------------------------------------- |
| c1   | 16    |                                           |
| c2   | 21    |                                           |
| c3   | 24    |                                           |
| c4   | 43    |                                           |
| lr   | 2860  | a base line number for READing DATA lines |
| wv   | 70    | game speed (I think)                      |
| w    | 51    | the number of nouns we know               |
| v    | 42    | the number of verbs we know               |
| g    | 2     |                                           |
| f    | 2     |                                           |

Constant strings

| Name | Value                                                   |
| ---- | ------------------------------------------------------- |
| g$   | `--------------------------------`                      |
| j$   | `THE STONES ARE FIXED`                                  |
| k$   | `REFLECTIONS STIR WITHIN`                               |
| l$   | `REMEMBER ALADDIN IT WORKED FOR HIM`                    |
| m$   | `DECIDE TO HAVE A LITTLE FUN AND `                      |
| n$   | `THE TORCH BRIGHTENS`                                   |
| o$   | `WHICH TAKES OMEGAN IN ITS CLAWS AND FLIES AWAY`        |
| p$   | `REMEMBER OLD TIMES`                                    |
| q$   | `90101191001109109000901000111000000100000010000000000` |
| r$   | ` WHICH FLIES YOU TO A REMOTE PLACE`                    |
| s$   | `FALLING UNDER THE SPELL OF THE BOATMAN `               |
| t$   | `AND ARE TAKEN TO THE ISLAND OF SECRETS`                |
| u$   | `YOU ANGER THE BIRD`                                    |
| v$   | `N??S??E??W??GO?GETTAKGIV` ... (verbs)                  |
| w$   | `YOU CAN'T `                                            |
| z$   | `APPEGGFLOJUGRAGPARTORPEB` ... (nouns)                  |


-----

## Word list

### Verbs
| id  | verb    | subroutine |
| --- | ------- | ---------- |
| 1   | N       | 810        |
| 2   | S       | 810        |
| 3   | E       | 810        |
| 4   | W       | 810        |
| 5   | GO      | 810        |
| 6   | GET     | 1080       |
| 7   | TAKE    | 1080       |
| 8   | GIVE    | 1390       |
| 9   | DROP    | 1530       |
| 10  | LEAVE   | 1540       |
| 11  | EAT     | 1630       |
| 12  | DRINK   | 1670       |
| 13  | RIDE    | 1710       |
| 14  | OPEN    | 1730       |
| 15  | PICK    | 1080       |
| 16  | CHOP    | 1760       |
| 17  | CHIP    | 1760       |
| 18  | TAP     | 1760       |
| 19  | BREAK   | 1760       |
| 20  | FIGHT   | 1820       |
| 21  | STRIKE  | 1820       |
| 22  | ATTACK  | 1820       |
| 23  | HIT     | 1820       |
| 24  | KILL    | 1910       |
| 25  | SWIM    | 2100       |
| 26  | SHELTER | 2210       |
| 27  | HELP    | 2270       |
| 28  | SCRATCH | 2270       |
| 29  | CATCH   | 1080       |
| 30  | RUB     | 2500       |
| 31  | POLISH  | 2500       |
| 32  | READ    | 2300       |
| 33  | EXAMINE | 2300       |
| 34  | FILL    | 2330       |
| 35  | SAY     | 2350       |
| 36  | WAIT    | 2400       |
| 37  | REST    | 2400       |
| 38  | WAVE    | 2470       |
| 39  | INFO    | 2540       |
| 40  | XLOAD   | 2600       |
| 41  | XSAVE   | 2600       |
| 42  | QUIT    | 2720       |
| 43  |         | 640        |

### Nouns

| ID  | name                                       | init `l` | init `f` | constant |
| --- | ------------------------------------------ | -------- | -------- | -------- |
| 1   | APPLE                                      | 45       | 9        |          |
| 2   | EGG                                        | 46       | 0        |          |
| 3   | FLOWER                                     | 71       | 1        |          |
| 4   | JUG                                        | 41       | 0        |          |
| 5   | RAG                                        | 44       | 1        |          |
| 6   | PARCHMENT                                  | 21       | 1        |          |
| 7   | TORCH                                      | 27       | 9        |          |
| 8   | PEBBLE                                     | 15       | 1        |          |
| 9   | AXE                                        | 53       | 0        |          |
| 10  | ROPE                                       | 62       | 0        |          |
| 11  | STAFF                                      | 75       | 1        |          |
| 12  | CHIP                                       | 58       | 1        |          |
| 13  | COAL                                       | 80       | 0        |          |
| 14  | FLINT                                      | 67       | 9        |          |
| 15  | HAMMER                                     | 44       | 1        |          |
| 16  | CANYON BEAST                               | 5        | 0        | c1       |
| 17  | LOAF                                       | 44       | 9        |          |
| 18  | MELON                                      | 42       | 0        |          |
| 19  | BISCUITS                                   | 60       | 0        |          |
| 20  | MUSHROOMS                                  | 21       | 0        |          |
| 21  | BOTTLE                                     | 44       | 9        | c2       |
| 22  | WINE                                       | 42       | 0        |          |
| 23  | SAP                                        | 77       | 1        |          |
| 24  | WATER                                      | 13       | 0        | c3       |
| 25  | BOATMAN                                    | 33       | 0        |          |
| 26  | CHEST                                      | 44       | 0        |          |
| 27  | COLUMN                                     | 58       | 1        |          |
| 28  | STONE                                      | 15       | 1        |          |
| 29  | TRAPDOOR                                   | 51       | 1        |          |
| 30  | VILLAGER                                   | 75       | 0        |          |
| 31  | LIQUOR                                     | 41       | 0        |          |
| 32  | SWAMPMAN                                   | 78       | 0        |          |
| 33  | SAGE                                       | 71       | 0        |          |
| 34  | BOOKS                                      | 50       | 0        |          |
| 35  | ROOTS                                      | 77       | 0        |          |
| 36  | ASA (Fierce living storm that follows you) | 23       | 1        |          |
| 37  | WRAITHS                                    | 19       | 0        |          |
| 38  | CLOAK                                      | 10       | 0        |          |
| 39  | OMEGAN                                     | 10       | 0        |          |
| 40  | SNAKE                                      | 45       | 0        |          |
| 41  | LOGMEN                                     | 42       | 0        |          |
| 42  | SCAVENGER                                  | 38       | 0        |          |
| 43  | MEDIAN                                     | 38       | 1        | c4       |
| 44  | NORTH                                      | 0        | 0        |          |
| 45  | SOUTH                                      | 0        | 0        |          |
| 46  | EAST                                       | 0        | 0        |          |
| 47  | WEST                                       | 0        | 0        |          |
| 48  | UP                                         | 0        | 0        |          |
| 49  | DOWN                                       | 0        | 0        |          |
| 50  | IN                                         | 0        | 0        |          |
| 51  | OUT                                        | 0        | 0        |          |



### Prepositions
I think these are mostly used for location descriptions.

1. BY
2. FACING
3. AT
4. IN
5. OUTSIDE
6. BENEATH
7. ON

## Location list
|     | Location                                           | N   | S   | W   | E   |
| --- | -------------------------------------------------- | --- | --- | --- | --- |
| 1   | THE FURTHEST DEPTHS OF THE FOREST                  | X   |     | X   |     |
| 2   | THE DEPTHS OF THE MUTANT FOREST                    | X   |     |     |     |
| 3   | A PATH OUT OF THE OVERGROWN DEPTHS                 | X   |     |     |     |
| 4   | A CARNIVOROUS TREE                                 | X   |     |     |     |
| 5   | A CORRAL BENEATH THE CRIMSON CANYON                | X   | X   |     | X   |
| 6   | THE TOP OF A STEEP CLIFF                           | X   |     | X   | X   |
| 7   | THE MARSH FACTORY                                  | X   |     | X   |     |
| 8   | THE SLUDGE FERMENTATION VATS                       | X   | X   |     | X   |
| 9   | THE UPPERMOST BATTLEMENTS                          | X   |     | X   |     |
| 10  | OMEGAN'S SANCTUM                                   | X   | X   |     | X   |
| 11  | SNELM'S LAIR                                       |     |     | X   |     |
| 12  | A DARK CAVE                                        |     |     |     |     |
| 13  | BROKEN BRANCHES                                    |     | X   |     |     |
| 14  | A THICKET OF BITING BUSHES                         |     |     |     |     |
| 15  | A HUGE GLASS STONE                                 | X   | X   |     | X   |
| 16  | THE EDGE OF CRIMSON CANYON                         |     |     | X   | X   |
| 17  | THE CLONE FACTORY                                  |     | X   | X   |     |
| 18  | A CORRIDOR OF CLONE STORAGE CASKS                  | X   | X   |     |     |
| 19  | EDGE OF THE WELL                                   |     |     |     |     |
| 20  | THE ROOM OF SECRET VISIONS                         | X   | X   |     | X   |
| 21  | SNELM'S INNER CHAMBER                              |     | X   | X   | X   |
| 22  | THE SOUTHERN EDGE OF THE FOREST                    |     | X   | X   |     |
| 23  | A LEAFY PATH                                       | X   |     |     |     |
| 24  | A FORK IN THE PATH                                 |     | X   |     |     |
| 25  | AN APPARENTLY UNCLIMBABLE ROCKY PATH               | X   | X   |     |     |
| 26  | A LEDGE ATOP THE CRIMSON CANYON                    |     |     |     | X   |
| 27  | A TALL ENTRANCE CHAMBER                            | X   | X   | X   |     |
| 28  | A LOW PASSAGE WITH ARMS REACHING FROM THE WALLS    | X   |     |     | X   |
| 29  | THE APPROACH TO THE WELL OF DESPAIR                |     |     | X   |     |
| 30  | A DIM CORRIDOR DEEP IN THE CASTLE                  | X   |     |     | X   |
| 31  | THE STAGNANT WATERS OF THE CRAWLING CREEK          | X   |     | X   |     |
| 32  | A SHALLOW POOL OFF THE CREEK                       | X   | X   |     |     |
| 33  | A LOG PIER, JUTTING OUT OVER THE CREEK             |     |     |     |     |
| 34  | A STRETCH OF FEATURELESS DUNES                     | X   | X   |     |     |
| 35  | A GROUP OF TALL TREES                              | X   |     |     | X   |
| 36  | A NARROW LEDGE AT THE SUMMIT OF THE CANYON         |     |     | X   | X   |
| 37  | A MONSTEROUS PORTAL IN THE CASTLE WALL             |     |     | X   | X   |
| 38  | A CHAMBER INCHES DEEP WITH DUST                    |     |     | X   |     |
| 39  | HERE                                               | X   | X   | X   | X   |
| 40  | A CARVED ARCHWAY                                   |     |     |     | X   |
| 41  | A SMALL HUT IN THE LOG SETTLEMENT                  |     | X   | X   | X   |
| 42  | A HUGE SPLIT-LOG TABLE                             | X   |     | X   |     |
| 43  | THE PORCH OF THE LOGMEN'S CABIN                    |     | X   |     | X   |
| 44  | GRANDPA'S SHACK                                    | X   | X   | X   |     |
| 45  | A CLEARING IN THE TREES BY A RICKETY SHACK         |     |     |     | X   |
| 46  | THE NEST OF A HUGE DACTYL                          |     | X   | X   | X   |
| 47  | THE CASTLE OF DARK SECRETS BY TWO HUGE STONES      |     |     | X   | X   |
| 48  | A ROOM LITTERED WITH BONES                         |     | X   | X   | X   |
| 49  | THE CELL OF WHISPERED SECRETS                      |     | X   | X   | X   |
| 50  | THE LIBRARY OF WRITTEN SECRETS                     |     | X   | X   | X   |
| 51  | A REFUSE STREWN STOREROOM                          | X   | X   | X   | X   |
| 52  | THE LOGMEN'S HALL                                  |     |     |     |     |
| 53  | A LOG BUILDING                                     | X   |     |     |     |
| 54  | A RUTTED HILLSIDE                                  | X   | X   |     |     |
| 55  | A WINDSWEPT PLAIN AMONGST STONE MEGALITHS          |     | X   |     |     |
| 56  | THE STEPS OF AN ANCIENT PYRAMID                    | X   |     |     | X   |
| 57  | THE ISLAND OF SECRETS                              |     | X   | X   | X   |
| 58  | A BROKEN MARBLE COLUMN                             | X   |     | X   |     |
| 59  | AN EXPANSE OF CRACKED, BAKED EARTH                 | X   | X   |     |     |
| 60  | A DESERTED ADOBE HUT                               | X   |     |     | X   |
| 61  | A LIVID GROWTH OF MAD ORCHIDS                      | X   |     | X   | X   |
| 62  | A CORNER STREWN WITH BROKEN CHAIRS                 |     | X   | X   | X   |
| 63  | THE BRIDGE NEAR TO A LOG SETTLEMENT                |     |     | X   | X   |
| 64  | A CRUMBLING MASS OF PETRIFIED TREES                | X   |     | X   | X   |
| 65  | THE EDGE OF THE PYRAMID                            | X   | X   | X   |     |
| 66  | THE ROOF OF THE ANCIENT PYRAMID                    |     | X   |     |     |
| 67  | AN IMPASSABLE SPLIT IN THE PYRAMID                 | X   | X   |     | X   |
| 68  | A BARREN BLASTED WASTELAND                         |     |     | X   |     |
| 69  | AN EXPANSE OF BLEAK, BURNT LAND                    | X   | X   |     |     |
| 70  | A DELAPIDATED ADOBE HUT                            |     | X   |     | X   |
| 71  | THE HEART OF THE LILIES                            |     | X   | X   |     |
| 72  | THE MIDST OF THE LILIES                            | X   | X   |     |     |
| 73  | A RIVER'S EDGE BY A LOG BRIDGE                     |     | X   |     |     |
| 74  | A PETRIFIED VILLAGE BY A RIVER CROWDED WITH LILIES |     | X   |     |     |
| 75  | THE REMAINS OF A VILLAGE                           | X   | X   |     |     |
| 76  | THE ENTRANCE TO A PETRIFIED VILLAGE                | X   | X   |     |     |
| 77  | A SWAMP MATTED WITH FIBROUS ROOTS                  | X   | X   |     |     |
| 78  | A VILLAGE OF HOLLOW STUMPS DEFYING THE SWAMP       |     | X   |     |     |
| 79  | A TUNNEL INTO ONE OF THE TREE STUMPS               | X   | X   |     |     |
| 80  | A HOLLOW CHAMBER MANY METRES IN DIAMETER           | X   | X   |     | X   |


## b$ states

b$ holds a 'coded' string indicating a particular state which is used to determine lots of conditions at once. Here is a list of what all of the possible states are

| b$      | State                                                                            |
| ------- | -------------------------------------------------------------------------------- |
| 10045   | Using the apple by the shack                                                     |
| 40041   | Interacting with the jug while in the hut                                        |
| 246046  | Using water at the Dactyl's nest                                                 |
| 480056  | Going 'up' while at the steps to the pyramid                                     |
| 490051  | Going 'down' while in the Logmen's store room                                    |
| 490066  | Going 'down' while on the roof of the pyramid                                    |
| 500012  | Going 'in' while in a dark cave,                                                 |
| 500037  | Going 'in' while by the portal in the wall                                       |
| 500045  | Going 'in' while in the clearing by the shack                                    |
| 500053  | Going 'in' while In the log building                                             |
| 500070  | Going 'in' while outside the adobe hut                                           |
| 510011  | Going 'out' while in Snelm's Lair                                                |
| 510041  | Going 'out' while in the log hut                                                 |
| 510043  | Going 'out' while in the porch of the cabin                                      |
| 510044  | Going 'out' while in Grandpa's shack                                             |
| 510052  | Going 'out' while in the Logmen's hall                                           |
| 510060  | Going 'out' while in the adobe hut                                               |
| 1258158 | Interacting with the chip in its initial state by the column                     |
| 2413075 | Interacting with the water in its initial state in the village                   |
| 2644044 | Interacting with the chest in its initial state while in the shack               |
| 2758158 | Interacting with the column in its initial state while standing next to it       |
| 2951151 | Interacting with the trapdoor in its initial state while in the storeroom        |
| 3075075 | Interacting with the villager in their initial state while in the village        |
| 3371071 | Interacting with the Sage in her initial state while at the heart of the lillies |
| 3450050 | Interacting with the books in their initial state while in the library           |
| 3577077 | Interacting with the roots in their initial state while in the swamp             |
| 3810010 | Interacting with the cloak in its initial state while in Omegan's sanctum        |




-----

## Solution 
https://ready64.org/giochi/soluzioni/island_of_secrets_sol.txt
