TABLE 		= TABLE_C_S6A_HR_B_S6JTEX

CYCLE_DEBUT	= 42
CYCLE_FIN	= 79
TRACE_DEBUT	= 1
TRACE_FIN	= 254

ORF		= C_S6A_HR_ORF.dat
VERBOSE		= 2

ID_LAT		= LATITUDE
ID_LON		= LONGITUDE

#################################

ALGO      	= ABAQUE_2D
ID_CHAMP  	= SSB_TEMP_1
PARAM_ALGO	= /home/hlafargue/ssb_fortran/Table_maj_BEM_S6_HR_SSB_TMP1.par | B | 1 | 1 | SSB_CORRECTION_PRINCIPAL_COMPONENT_2 | SSB_CORRECTION_PRINCIPAL_COMPONENT_1

#################################

ALGO      	= ABAQUE_2D
ID_CHAMP  	= SSB_TEMP_2
PARAM_ALGO	= /home/hlafargue/ssb_fortran/Table_maj_BEM_S6_HR_SSB_TMP2.par | B | 1 | 1 | SSB_CORRECTION_PRINCIPAL_COMPONENT_2 | SSB_CORRECTION_PRINCIPAL_COMPONENT_1

#################################

ALGO      	= ABAQUE_2D
ID_CHAMP  	= SSB_TEMP_3
PARAM_ALGO	= /home/hlafargue/ssb_fortran/Table_maj_BEM_S6_HR_SSB_TMP3.par | B | 1 | 1 | SSB_CORRECTION_PRINCIPAL_COMPONENT_2 | SSB_CORRECTION_PRINCIPAL_COMPONENT_1

#################################

ALGO      	= ABAQUE_2D
ID_CHAMP  	= SSB_TEMP_4
PARAM_ALGO	= /home/hlafargue/ssb_fortran/Table_maj_BEM_S6_HR_SSB_TMP4.par | B | 1 | 1 | SSB_CORRECTION_PRINCIPAL_COMPONENT_2 | SSB_CORRECTION_PRINCIPAL_COMPONENT_1

#################################

ALGO      	= ABAQUE_2D
ID_CHAMP  	= SSB_REF
PARAM_ALGO	= /home/hlafargue/ssb_fortran/Table_maj_BEM_S6_HR_SSB_REF.par | B | m | m/s | SWH.ALTI | WIND_SPEED.ALTI
