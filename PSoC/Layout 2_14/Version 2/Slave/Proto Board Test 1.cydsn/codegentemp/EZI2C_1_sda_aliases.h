/*******************************************************************************
* File Name: EZI2C_1_sda.h  
* Version 2.20
*
* Description:
*  This file contains the Alias definitions for Per-Pin APIs in cypins.h. 
*  Information on using these APIs can be found in the System Reference Guide.
*
* Note:
*
********************************************************************************
* Copyright 2008-2015, Cypress Semiconductor Corporation.  All rights reserved.
* You may use this file only in accordance with the license, terms, conditions, 
* disclaimers, and limitations in the end user license agreement accompanying 
* the software package with which this file was provided.
*******************************************************************************/

#if !defined(CY_PINS_EZI2C_1_sda_ALIASES_H) /* Pins EZI2C_1_sda_ALIASES_H */
#define CY_PINS_EZI2C_1_sda_ALIASES_H

#include "cytypes.h"
#include "cyfitter.h"
#include "cypins.h"


/***************************************
*              Constants        
***************************************/
#define EZI2C_1_sda_0			(EZI2C_1_sda__0__PC)
#define EZI2C_1_sda_0_PS		(EZI2C_1_sda__0__PS)
#define EZI2C_1_sda_0_PC		(EZI2C_1_sda__0__PC)
#define EZI2C_1_sda_0_DR		(EZI2C_1_sda__0__DR)
#define EZI2C_1_sda_0_SHIFT	(EZI2C_1_sda__0__SHIFT)
#define EZI2C_1_sda_0_INTR	((uint16)((uint16)0x0003u << (EZI2C_1_sda__0__SHIFT*2u)))

#define EZI2C_1_sda_INTR_ALL	 ((uint16)(EZI2C_1_sda_0_INTR))


#endif /* End Pins EZI2C_1_sda_ALIASES_H */


/* [] END OF FILE */
