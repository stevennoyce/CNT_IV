/*******************************************************************************
* File Name: Pin_SolutionGate.h  
* Version 2.20
*
* Description:
*  This file contains Pin function prototypes and register defines
*
* Note:
*
********************************************************************************
* Copyright 2008-2015, Cypress Semiconductor Corporation.  All rights reserved.
* You may use this file only in accordance with the license, terms, conditions, 
* disclaimers, and limitations in the end user license agreement accompanying 
* the software package with which this file was provided.
*******************************************************************************/

#if !defined(CY_PINS_Pin_SolutionGate_H) /* Pins Pin_SolutionGate_H */
#define CY_PINS_Pin_SolutionGate_H

#include "cytypes.h"
#include "cyfitter.h"
#include "cypins.h"
#include "Pin_SolutionGate_aliases.h"

/* APIs are not generated for P15[7:6] */
#if !(CY_PSOC5A &&\
	 Pin_SolutionGate__PORT == 15 && ((Pin_SolutionGate__MASK & 0xC0) != 0))


/***************************************
*        Function Prototypes             
***************************************/    

/**
* \addtogroup group_general
* @{
*/
void    Pin_SolutionGate_Write(uint8 value);
void    Pin_SolutionGate_SetDriveMode(uint8 mode);
uint8   Pin_SolutionGate_ReadDataReg(void);
uint8   Pin_SolutionGate_Read(void);
void    Pin_SolutionGate_SetInterruptMode(uint16 position, uint16 mode);
uint8   Pin_SolutionGate_ClearInterrupt(void);
/** @} general */

/***************************************
*           API Constants        
***************************************/
/**
* \addtogroup group_constants
* @{
*/
    /** \addtogroup driveMode Drive mode constants
     * \brief Constants to be passed as "mode" parameter in the Pin_SolutionGate_SetDriveMode() function.
     *  @{
     */
        #define Pin_SolutionGate_DM_ALG_HIZ         PIN_DM_ALG_HIZ
        #define Pin_SolutionGate_DM_DIG_HIZ         PIN_DM_DIG_HIZ
        #define Pin_SolutionGate_DM_RES_UP          PIN_DM_RES_UP
        #define Pin_SolutionGate_DM_RES_DWN         PIN_DM_RES_DWN
        #define Pin_SolutionGate_DM_OD_LO           PIN_DM_OD_LO
        #define Pin_SolutionGate_DM_OD_HI           PIN_DM_OD_HI
        #define Pin_SolutionGate_DM_STRONG          PIN_DM_STRONG
        #define Pin_SolutionGate_DM_RES_UPDWN       PIN_DM_RES_UPDWN
    /** @} driveMode */
/** @} group_constants */
    
/* Digital Port Constants */
#define Pin_SolutionGate_MASK               Pin_SolutionGate__MASK
#define Pin_SolutionGate_SHIFT              Pin_SolutionGate__SHIFT
#define Pin_SolutionGate_WIDTH              1u

/* Interrupt constants */
#if defined(Pin_SolutionGate__INTSTAT)
/**
* \addtogroup group_constants
* @{
*/
    /** \addtogroup intrMode Interrupt constants
     * \brief Constants to be passed as "mode" parameter in Pin_SolutionGate_SetInterruptMode() function.
     *  @{
     */
        #define Pin_SolutionGate_INTR_NONE      (uint16)(0x0000u)
        #define Pin_SolutionGate_INTR_RISING    (uint16)(0x0001u)
        #define Pin_SolutionGate_INTR_FALLING   (uint16)(0x0002u)
        #define Pin_SolutionGate_INTR_BOTH      (uint16)(0x0003u) 
    /** @} intrMode */
/** @} group_constants */

    #define Pin_SolutionGate_INTR_MASK      (0x01u) 
#endif /* (Pin_SolutionGate__INTSTAT) */


/***************************************
*             Registers        
***************************************/

/* Main Port Registers */
/* Pin State */
#define Pin_SolutionGate_PS                     (* (reg8 *) Pin_SolutionGate__PS)
/* Data Register */
#define Pin_SolutionGate_DR                     (* (reg8 *) Pin_SolutionGate__DR)
/* Port Number */
#define Pin_SolutionGate_PRT_NUM                (* (reg8 *) Pin_SolutionGate__PRT) 
/* Connect to Analog Globals */                                                  
#define Pin_SolutionGate_AG                     (* (reg8 *) Pin_SolutionGate__AG)                       
/* Analog MUX bux enable */
#define Pin_SolutionGate_AMUX                   (* (reg8 *) Pin_SolutionGate__AMUX) 
/* Bidirectional Enable */                                                        
#define Pin_SolutionGate_BIE                    (* (reg8 *) Pin_SolutionGate__BIE)
/* Bit-mask for Aliased Register Access */
#define Pin_SolutionGate_BIT_MASK               (* (reg8 *) Pin_SolutionGate__BIT_MASK)
/* Bypass Enable */
#define Pin_SolutionGate_BYP                    (* (reg8 *) Pin_SolutionGate__BYP)
/* Port wide control signals */                                                   
#define Pin_SolutionGate_CTL                    (* (reg8 *) Pin_SolutionGate__CTL)
/* Drive Modes */
#define Pin_SolutionGate_DM0                    (* (reg8 *) Pin_SolutionGate__DM0) 
#define Pin_SolutionGate_DM1                    (* (reg8 *) Pin_SolutionGate__DM1)
#define Pin_SolutionGate_DM2                    (* (reg8 *) Pin_SolutionGate__DM2) 
/* Input Buffer Disable Override */
#define Pin_SolutionGate_INP_DIS                (* (reg8 *) Pin_SolutionGate__INP_DIS)
/* LCD Common or Segment Drive */
#define Pin_SolutionGate_LCD_COM_SEG            (* (reg8 *) Pin_SolutionGate__LCD_COM_SEG)
/* Enable Segment LCD */
#define Pin_SolutionGate_LCD_EN                 (* (reg8 *) Pin_SolutionGate__LCD_EN)
/* Slew Rate Control */
#define Pin_SolutionGate_SLW                    (* (reg8 *) Pin_SolutionGate__SLW)

/* DSI Port Registers */
/* Global DSI Select Register */
#define Pin_SolutionGate_PRTDSI__CAPS_SEL       (* (reg8 *) Pin_SolutionGate__PRTDSI__CAPS_SEL) 
/* Double Sync Enable */
#define Pin_SolutionGate_PRTDSI__DBL_SYNC_IN    (* (reg8 *) Pin_SolutionGate__PRTDSI__DBL_SYNC_IN) 
/* Output Enable Select Drive Strength */
#define Pin_SolutionGate_PRTDSI__OE_SEL0        (* (reg8 *) Pin_SolutionGate__PRTDSI__OE_SEL0) 
#define Pin_SolutionGate_PRTDSI__OE_SEL1        (* (reg8 *) Pin_SolutionGate__PRTDSI__OE_SEL1) 
/* Port Pin Output Select Registers */
#define Pin_SolutionGate_PRTDSI__OUT_SEL0       (* (reg8 *) Pin_SolutionGate__PRTDSI__OUT_SEL0) 
#define Pin_SolutionGate_PRTDSI__OUT_SEL1       (* (reg8 *) Pin_SolutionGate__PRTDSI__OUT_SEL1) 
/* Sync Output Enable Registers */
#define Pin_SolutionGate_PRTDSI__SYNC_OUT       (* (reg8 *) Pin_SolutionGate__PRTDSI__SYNC_OUT) 

/* SIO registers */
#if defined(Pin_SolutionGate__SIO_CFG)
    #define Pin_SolutionGate_SIO_HYST_EN        (* (reg8 *) Pin_SolutionGate__SIO_HYST_EN)
    #define Pin_SolutionGate_SIO_REG_HIFREQ     (* (reg8 *) Pin_SolutionGate__SIO_REG_HIFREQ)
    #define Pin_SolutionGate_SIO_CFG            (* (reg8 *) Pin_SolutionGate__SIO_CFG)
    #define Pin_SolutionGate_SIO_DIFF           (* (reg8 *) Pin_SolutionGate__SIO_DIFF)
#endif /* (Pin_SolutionGate__SIO_CFG) */

/* Interrupt Registers */
#if defined(Pin_SolutionGate__INTSTAT)
    #define Pin_SolutionGate_INTSTAT            (* (reg8 *) Pin_SolutionGate__INTSTAT)
    #define Pin_SolutionGate_SNAP               (* (reg8 *) Pin_SolutionGate__SNAP)
    
	#define Pin_SolutionGate_0_INTTYPE_REG 		(* (reg8 *) Pin_SolutionGate__0__INTTYPE)
#endif /* (Pin_SolutionGate__INTSTAT) */

#endif /* CY_PSOC5A... */

#endif /*  CY_PINS_Pin_SolutionGate_H */


/* [] END OF FILE */
