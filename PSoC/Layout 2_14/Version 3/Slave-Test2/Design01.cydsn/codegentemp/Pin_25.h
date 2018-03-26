/*******************************************************************************
* File Name: Pin_25.h  
* Version 2.20
*
* Description:
*  This file contains Pin function prototypes and register defines
*
********************************************************************************
* Copyright 2008-2015, Cypress Semiconductor Corporation.  All rights reserved.
* You may use this file only in accordance with the license, terms, conditions, 
* disclaimers, and limitations in the end user license agreement accompanying 
* the software package with which this file was provided.
*******************************************************************************/

#if !defined(CY_PINS_Pin_25_H) /* Pins Pin_25_H */
#define CY_PINS_Pin_25_H

#include "cytypes.h"
#include "cyfitter.h"
#include "Pin_25_aliases.h"


/***************************************
*     Data Struct Definitions
***************************************/

/**
* \addtogroup group_structures
* @{
*/
    
/* Structure for sleep mode support */
typedef struct
{
    uint32 pcState; /**< State of the port control register */
    uint32 sioState; /**< State of the SIO configuration */
    uint32 usbState; /**< State of the USBIO regulator */
} Pin_25_BACKUP_STRUCT;

/** @} structures */


/***************************************
*        Function Prototypes             
***************************************/
/**
* \addtogroup group_general
* @{
*/
uint8   Pin_25_Read(void);
void    Pin_25_Write(uint8 value);
uint8   Pin_25_ReadDataReg(void);
#if defined(Pin_25__PC) || (CY_PSOC4_4200L) 
    void    Pin_25_SetDriveMode(uint8 mode);
#endif
void    Pin_25_SetInterruptMode(uint16 position, uint16 mode);
uint8   Pin_25_ClearInterrupt(void);
/** @} general */

/**
* \addtogroup group_power
* @{
*/
void Pin_25_Sleep(void); 
void Pin_25_Wakeup(void);
/** @} power */


/***************************************
*           API Constants        
***************************************/
#if defined(Pin_25__PC) || (CY_PSOC4_4200L) 
    /* Drive Modes */
    #define Pin_25_DRIVE_MODE_BITS        (3)
    #define Pin_25_DRIVE_MODE_IND_MASK    (0xFFFFFFFFu >> (32 - Pin_25_DRIVE_MODE_BITS))

    /**
    * \addtogroup group_constants
    * @{
    */
        /** \addtogroup driveMode Drive mode constants
         * \brief Constants to be passed as "mode" parameter in the Pin_25_SetDriveMode() function.
         *  @{
         */
        #define Pin_25_DM_ALG_HIZ         (0x00u) /**< \brief High Impedance Analog   */
        #define Pin_25_DM_DIG_HIZ         (0x01u) /**< \brief High Impedance Digital  */
        #define Pin_25_DM_RES_UP          (0x02u) /**< \brief Resistive Pull Up       */
        #define Pin_25_DM_RES_DWN         (0x03u) /**< \brief Resistive Pull Down     */
        #define Pin_25_DM_OD_LO           (0x04u) /**< \brief Open Drain, Drives Low  */
        #define Pin_25_DM_OD_HI           (0x05u) /**< \brief Open Drain, Drives High */
        #define Pin_25_DM_STRONG          (0x06u) /**< \brief Strong Drive            */
        #define Pin_25_DM_RES_UPDWN       (0x07u) /**< \brief Resistive Pull Up/Down  */
        /** @} driveMode */
    /** @} group_constants */
#endif

/* Digital Port Constants */
#define Pin_25_MASK               Pin_25__MASK
#define Pin_25_SHIFT              Pin_25__SHIFT
#define Pin_25_WIDTH              1u

/**
* \addtogroup group_constants
* @{
*/
    /** \addtogroup intrMode Interrupt constants
     * \brief Constants to be passed as "mode" parameter in Pin_25_SetInterruptMode() function.
     *  @{
     */
        #define Pin_25_INTR_NONE      ((uint16)(0x0000u)) /**< \brief Disabled             */
        #define Pin_25_INTR_RISING    ((uint16)(0x5555u)) /**< \brief Rising edge trigger  */
        #define Pin_25_INTR_FALLING   ((uint16)(0xaaaau)) /**< \brief Falling edge trigger */
        #define Pin_25_INTR_BOTH      ((uint16)(0xffffu)) /**< \brief Both edge trigger    */
    /** @} intrMode */
/** @} group_constants */

/* SIO LPM definition */
#if defined(Pin_25__SIO)
    #define Pin_25_SIO_LPM_MASK       (0x03u)
#endif

/* USBIO definitions */
#if !defined(Pin_25__PC) && (CY_PSOC4_4200L)
    #define Pin_25_USBIO_ENABLE               ((uint32)0x80000000u)
    #define Pin_25_USBIO_DISABLE              ((uint32)(~Pin_25_USBIO_ENABLE))
    #define Pin_25_USBIO_SUSPEND_SHIFT        CYFLD_USBDEVv2_USB_SUSPEND__OFFSET
    #define Pin_25_USBIO_SUSPEND_DEL_SHIFT    CYFLD_USBDEVv2_USB_SUSPEND_DEL__OFFSET
    #define Pin_25_USBIO_ENTER_SLEEP          ((uint32)((1u << Pin_25_USBIO_SUSPEND_SHIFT) \
                                                        | (1u << Pin_25_USBIO_SUSPEND_DEL_SHIFT)))
    #define Pin_25_USBIO_EXIT_SLEEP_PH1       ((uint32)~((uint32)(1u << Pin_25_USBIO_SUSPEND_SHIFT)))
    #define Pin_25_USBIO_EXIT_SLEEP_PH2       ((uint32)~((uint32)(1u << Pin_25_USBIO_SUSPEND_DEL_SHIFT)))
    #define Pin_25_USBIO_CR1_OFF              ((uint32)0xfffffffeu)
#endif


/***************************************
*             Registers        
***************************************/
/* Main Port Registers */
#if defined(Pin_25__PC)
    /* Port Configuration */
    #define Pin_25_PC                 (* (reg32 *) Pin_25__PC)
#endif
/* Pin State */
#define Pin_25_PS                     (* (reg32 *) Pin_25__PS)
/* Data Register */
#define Pin_25_DR                     (* (reg32 *) Pin_25__DR)
/* Input Buffer Disable Override */
#define Pin_25_INP_DIS                (* (reg32 *) Pin_25__PC2)

/* Interrupt configuration Registers */
#define Pin_25_INTCFG                 (* (reg32 *) Pin_25__INTCFG)
#define Pin_25_INTSTAT                (* (reg32 *) Pin_25__INTSTAT)

/* "Interrupt cause" register for Combined Port Interrupt (AllPortInt) in GSRef component */
#if defined (CYREG_GPIO_INTR_CAUSE)
    #define Pin_25_INTR_CAUSE         (* (reg32 *) CYREG_GPIO_INTR_CAUSE)
#endif

/* SIO register */
#if defined(Pin_25__SIO)
    #define Pin_25_SIO_REG            (* (reg32 *) Pin_25__SIO)
#endif /* (Pin_25__SIO_CFG) */

/* USBIO registers */
#if !defined(Pin_25__PC) && (CY_PSOC4_4200L)
    #define Pin_25_USB_POWER_REG       (* (reg32 *) CYREG_USBDEVv2_USB_POWER_CTRL)
    #define Pin_25_CR1_REG             (* (reg32 *) CYREG_USBDEVv2_CR1)
    #define Pin_25_USBIO_CTRL_REG      (* (reg32 *) CYREG_USBDEVv2_USB_USBIO_CTRL)
#endif    
    
    
/***************************************
* The following code is DEPRECATED and 
* must not be used in new designs.
***************************************/
/**
* \addtogroup group_deprecated
* @{
*/
#define Pin_25_DRIVE_MODE_SHIFT       (0x00u)
#define Pin_25_DRIVE_MODE_MASK        (0x07u << Pin_25_DRIVE_MODE_SHIFT)
/** @} deprecated */

#endif /* End Pins Pin_25_H */


/* [] END OF FILE */
