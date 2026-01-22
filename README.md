# Chord-Progression-Generator
Simple Python script to generate chord progressions for different genres and musical keys.

Example input:
```
Enter Chord (e.g., F, Cmaj7, G/B): C
```
Output:
```
************************************************************
ANALYSIS: C Ionian
SCALE: C - D - E - F - G - A - B
************************************************************
Deg   Diatonic Context     Notes
--------------------------------------------------
1     CMaj7                 C, E, G, B
2     Dm7                   D, F, A, C
3     Em7                   E, G, B, D
4     FMaj7                 F, A, C, E
5     G7                    G, B, D, F
6     Am7                   A, C, E, G
7     Bm7b5                 B, D, F, A
--------------------------------------------------
Enter Genre for Progressions (Press Enter for All):
```
Input:
```
Enter Genre for Progressions (Press Enter for All): Rock
```
Output:
```
[Pop / Rock]
> Walkdown (I - V/vii - vi - IV)
  CMaj7 -> G7/B -> Am7 -> FMaj7
> Emotional (vi - IV - I - Vsus - V)
  Am7 -> FMaj7 -> CMaj7 -> Gsus4 -> G7
> Slash Climb (I - I/iii - IV)
  CMaj7 -> CMaj7/E -> FMaj7

[Rock / Metal]
> Pedal Point (I - bVII/I - bVI/I)
  CMaj7 -> Bm7b5/C -> Am7/C
> Grunge (I - bIII - IV)
  CMaj7 -> EMajor -> FMaj7
```
