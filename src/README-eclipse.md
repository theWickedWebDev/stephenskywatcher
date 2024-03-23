
"""
Example Base Setting choices:
f/8 ISO200
f/11 ISO100
f/12.6 ISO200
"""

"""
Pre Eclipse
  - Simple exposure on a long interval
    * Need to be able to +/- exposure

Partial Eclipse
  - Simple exposure on a long interval
    * Need to be able to +/- exposure

Baily's Beads (~30s before Totality)
  - Fast as I can bracketed exposures

Totality (4min 21sec)
    - Bracketed exposures
    * Slowly ramp up exposure to full corona shot at max totality
    ** Ramp values:
        - Start: 1/4000
        - End: [max totality exposure]

    == Buttons
        -Start Totality Button, ramps up shots [0:00 to 2:00]

    
MAX Totality (~40s)
    - 1 long exposure (8s 12s?) to capture Earthshine on Moon
    * Slowly ramp down exposure until Baily's beads (C3)
    ** Ramp values:
        - Start: [max totality exposure]
        - End: 1/4000
    
    == Buttons
        -Start Max Button, takes 5 exposures:
          5s  > 0:00-0:05
          7s  > 0:06-0:13
          10s > 0:14-0:24
          7s  > 0:25-0:32
          5s  > 0:33-0:38

Baily's Beads: [repeat above]
Partial Eclipse: [repeat above]
Post Exclipse: [repeat above]

*Gotcha* - Need a time either before or after max totality for a picture of people
          - probably needs to be a slightly longish exposure
"""

"""
TIMING: 4m21s (total)

(21s)
First Baily's Beads: -20s + (10s of totality)
Second Baily's Beads: (10s of totality) + 10s

Remaining for Totality: 4m

-----
-0:20: Baily's start
 #
 0:00: (Totality start)
 0:10: Baily's end
 #
 0:12: Ramp up start      (+10s start)
 1:42: Ramp up end        (-18s max)
 #
 1:44: Max Totality Start (-16s max)
 2:00: (Max Totality)
 2:16: Max Totality End   (+16s max)
 #
 2:18: Ramp down start    (+18s max)
 0:00: Ramp down end      (-10s start)
 #
+0:20: Baily's ends
"""
