Function JUMPHEIGHT(speed, hover)
JUMPHEIGHT = 0
FOR i = 1 TO hover
JUMPHEIGHT = JUMPHEIGHT + speed/8 * ((COS(2*Pi*i/(2*hover)) + 1)/2.5 + 0.2) * (hover - i + 1)
NEXT
End Function