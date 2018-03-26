/*******************************************************************************
* File Name: CommunicationTimer.h
* Version 2.80
*
*  Description:
*     Contains the function prototypes and constants available to the timer
*     user module.
*
*   Note:
*     None
*
********************************************************************************
* Copyright 2008-2017, Cypress Semiconductor Corporation.  All rights reserved.
* You may use this file only in accordance with the license, terms, conditions,
* disclaimers, and limitations in the end user license agreement accompanying
* the software package with which this file was provided.
********************************************************************************/

#if !defined(CY_TIMER_CommunicationTimer_H)
#define CY_TIMER_CommunicationTimer_H

#include "cytypes.h"
#include "cyfitter.h"
#include "CyLib.h" /* For CyEnterCriticalSection() and CyExitCriticalSection() functions */

extern uint8 CommunicationTimer_initVar;

/* Check to see if required defines such as CY_PSOC5LP are available */
/* They are defined starting with cy_boot v3.0 */
#if !defined (CY_PSOC5LP)
    #error Component Timer_v2_80 requires cy_boot v3.0 or later
#endif /* (CY_ PSOC5LP) */


/**************************************
*           Parameter Defaults
**************************************/

#define CommunicationTimer_Resolution                 8u
#define CommunicationTimer_UsingFixedFunction         1u
#define CommunicationTimer_UsingHWCaptureCounter      0u
#define CommunicationTimer_SoftwareCaptureMode        0u
#define CommunicationTimer_SoftwareTriggerMode        0u
#define CommunicationTimer_UsingHWEnable              0u
#define CommunicationTimer_EnableTriggerMode          0u
#define CommunicationTimer_InterruptOnCaptureCount    0u
#define CommunicationTimer_RunModeUsed                0u
#define CommunicationTimer_ControlRegRemoved          0u

#if defined(CommunicationTimer_TimerUDB_sCTRLReg_SyncCtl_ctrlreg__CONTROL_REG)
    #define CommunicationTimer_UDB_CONTROL_REG_REMOVED            (0u)
#elif  (CommunicationTimer_UsingFixedFunction)
    #define CommunicationTimer_UDB_CONTROL_REG_REMOVED            (0u)
#else 
    #define CommunicationTimer_UDB_CONTROL_REG_REMOVED            (1u)
#endif /* End CommunicationTimer_TimerUDB_sCTRLReg_SyncCtl_ctrlreg__CONTROL_REG */


/***************************************
*       Type defines
***************************************/


/**************************************************************************
 * Sleep Wakeup Backup structure for Timer Component
 *************************************************************************/
typedef struct
{
    uint8 TimerEnableState;
    #if(!CommunicationTimer_UsingFixedFunction)

        uint8 TimerUdb;
        uint8 InterruptMaskValue;
        #if (CommunicationTimer_UsingHWCaptureCounter)
            uint8 TimerCaptureCounter;
        #endif /* variable declarations for backing up non retention registers in CY_UDB_V1 */

        #if (!CommunicationTimer_UDB_CONTROL_REG_REMOVED)
            uint8 TimerControlRegister;
        #endif /* variable declaration for backing up enable state of the Timer */
    #endif /* define backup variables only for UDB implementation. Fixed function registers are all retention */

}CommunicationTimer_backupStruct;


/***************************************
*       Function Prototypes
***************************************/

void    CommunicationTimer_Start(void) ;
void    CommunicationTimer_Stop(void) ;

void    CommunicationTimer_SetInterruptMode(uint8 interruptMode) ;
uint8   CommunicationTimer_ReadStatusRegister(void) ;
/* Deprecated function. Do not use this in future. Retained for backward compatibility */
#define CommunicationTimer_GetInterruptSource() CommunicationTimer_ReadStatusRegister()

#if(!CommunicationTimer_UDB_CONTROL_REG_REMOVED)
    uint8   CommunicationTimer_ReadControlRegister(void) ;
    void    CommunicationTimer_WriteControlRegister(uint8 control) ;
#endif /* (!CommunicationTimer_UDB_CONTROL_REG_REMOVED) */

uint8  CommunicationTimer_ReadPeriod(void) ;
void    CommunicationTimer_WritePeriod(uint8 period) ;
uint8  CommunicationTimer_ReadCounter(void) ;
void    CommunicationTimer_WriteCounter(uint8 counter) ;
uint8  CommunicationTimer_ReadCapture(void) ;
void    CommunicationTimer_SoftwareCapture(void) ;

#if(!CommunicationTimer_UsingFixedFunction) /* UDB Prototypes */
    #if (CommunicationTimer_SoftwareCaptureMode)
        void    CommunicationTimer_SetCaptureMode(uint8 captureMode) ;
    #endif /* (!CommunicationTimer_UsingFixedFunction) */

    #if (CommunicationTimer_SoftwareTriggerMode)
        void    CommunicationTimer_SetTriggerMode(uint8 triggerMode) ;
    #endif /* (CommunicationTimer_SoftwareTriggerMode) */

    #if (CommunicationTimer_EnableTriggerMode)
        void    CommunicationTimer_EnableTrigger(void) ;
        void    CommunicationTimer_DisableTrigger(void) ;
    #endif /* (CommunicationTimer_EnableTriggerMode) */


    #if(CommunicationTimer_InterruptOnCaptureCount)
        void    CommunicationTimer_SetInterruptCount(uint8 interruptCount) ;
    #endif /* (CommunicationTimer_InterruptOnCaptureCount) */

    #if (CommunicationTimer_UsingHWCaptureCounter)
        void    CommunicationTimer_SetCaptureCount(uint8 captureCount) ;
        uint8   CommunicationTimer_ReadCaptureCount(void) ;
    #endif /* (CommunicationTimer_UsingHWCaptureCounter) */

    void CommunicationTimer_ClearFIFO(void) ;
#endif /* UDB Prototypes */

/* Sleep Retention APIs */
void CommunicationTimer_Init(void)          ;
void CommunicationTimer_Enable(void)        ;
void CommunicationTimer_SaveConfig(void)    ;
void CommunicationTimer_RestoreConfig(void) ;
void CommunicationTimer_Sleep(void)         ;
void CommunicationTimer_Wakeup(void)        ;


/***************************************
*   Enumerated Types and Parameters
***************************************/

/* Enumerated Type B_Timer__CaptureModes, Used in Capture Mode */
#define CommunicationTimer__B_TIMER__CM_NONE 0
#define CommunicationTimer__B_TIMER__CM_RISINGEDGE 1
#define CommunicationTimer__B_TIMER__CM_FALLINGEDGE 2
#define CommunicationTimer__B_TIMER__CM_EITHEREDGE 3
#define CommunicationTimer__B_TIMER__CM_SOFTWARE 4



/* Enumerated Type B_Timer__TriggerModes, Used in Trigger Mode */
#define CommunicationTimer__B_TIMER__TM_NONE 0x00u
#define CommunicationTimer__B_TIMER__TM_RISINGEDGE 0x04u
#define CommunicationTimer__B_TIMER__TM_FALLINGEDGE 0x08u
#define CommunicationTimer__B_TIMER__TM_EITHEREDGE 0x0Cu
#define CommunicationTimer__B_TIMER__TM_SOFTWARE 0x10u


/***************************************
*    Initialial Parameter Constants
***************************************/

#define CommunicationTimer_INIT_PERIOD             255u
#define CommunicationTimer_INIT_CAPTURE_MODE       ((uint8)((uint8)1u << CommunicationTimer_CTRL_CAP_MODE_SHIFT))
#define CommunicationTimer_INIT_TRIGGER_MODE       ((uint8)((uint8)0u << CommunicationTimer_CTRL_TRIG_MODE_SHIFT))
#if (CommunicationTimer_UsingFixedFunction)
    #define CommunicationTimer_INIT_INTERRUPT_MODE (((uint8)((uint8)1u << CommunicationTimer_STATUS_TC_INT_MASK_SHIFT)) | \
                                                  ((uint8)((uint8)0 << CommunicationTimer_STATUS_CAPTURE_INT_MASK_SHIFT)))
#else
    #define CommunicationTimer_INIT_INTERRUPT_MODE (((uint8)((uint8)1u << CommunicationTimer_STATUS_TC_INT_MASK_SHIFT)) | \
                                                 ((uint8)((uint8)0 << CommunicationTimer_STATUS_CAPTURE_INT_MASK_SHIFT)) | \
                                                 ((uint8)((uint8)0 << CommunicationTimer_STATUS_FIFOFULL_INT_MASK_SHIFT)))
#endif /* (CommunicationTimer_UsingFixedFunction) */
#define CommunicationTimer_INIT_CAPTURE_COUNT      (2u)
#define CommunicationTimer_INIT_INT_CAPTURE_COUNT  ((uint8)((uint8)(1u - 1u) << CommunicationTimer_CTRL_INTCNT_SHIFT))


/***************************************
*           Registers
***************************************/

#if (CommunicationTimer_UsingFixedFunction) /* Implementation Specific Registers and Register Constants */


    /***************************************
    *    Fixed Function Registers
    ***************************************/

    #define CommunicationTimer_STATUS         (*(reg8 *) CommunicationTimer_TimerHW__SR0 )
    /* In Fixed Function Block Status and Mask are the same register */
    #define CommunicationTimer_STATUS_MASK    (*(reg8 *) CommunicationTimer_TimerHW__SR0 )
    #define CommunicationTimer_CONTROL        (*(reg8 *) CommunicationTimer_TimerHW__CFG0)
    #define CommunicationTimer_CONTROL2       (*(reg8 *) CommunicationTimer_TimerHW__CFG1)
    #define CommunicationTimer_CONTROL2_PTR   ( (reg8 *) CommunicationTimer_TimerHW__CFG1)
    #define CommunicationTimer_RT1            (*(reg8 *) CommunicationTimer_TimerHW__RT1)
    #define CommunicationTimer_RT1_PTR        ( (reg8 *) CommunicationTimer_TimerHW__RT1)

    #if (CY_PSOC3 || CY_PSOC5LP)
        #define CommunicationTimer_CONTROL3       (*(reg8 *) CommunicationTimer_TimerHW__CFG2)
        #define CommunicationTimer_CONTROL3_PTR   ( (reg8 *) CommunicationTimer_TimerHW__CFG2)
    #endif /* (CY_PSOC3 || CY_PSOC5LP) */
    #define CommunicationTimer_GLOBAL_ENABLE  (*(reg8 *) CommunicationTimer_TimerHW__PM_ACT_CFG)
    #define CommunicationTimer_GLOBAL_STBY_ENABLE  (*(reg8 *) CommunicationTimer_TimerHW__PM_STBY_CFG)

    #define CommunicationTimer_CAPTURE_LSB         (* (reg16 *) CommunicationTimer_TimerHW__CAP0 )
    #define CommunicationTimer_CAPTURE_LSB_PTR       ((reg16 *) CommunicationTimer_TimerHW__CAP0 )
    #define CommunicationTimer_PERIOD_LSB          (* (reg16 *) CommunicationTimer_TimerHW__PER0 )
    #define CommunicationTimer_PERIOD_LSB_PTR        ((reg16 *) CommunicationTimer_TimerHW__PER0 )
    #define CommunicationTimer_COUNTER_LSB         (* (reg16 *) CommunicationTimer_TimerHW__CNT_CMP0 )
    #define CommunicationTimer_COUNTER_LSB_PTR       ((reg16 *) CommunicationTimer_TimerHW__CNT_CMP0 )


    /***************************************
    *    Register Constants
    ***************************************/

    /* Fixed Function Block Chosen */
    #define CommunicationTimer_BLOCK_EN_MASK                     CommunicationTimer_TimerHW__PM_ACT_MSK
    #define CommunicationTimer_BLOCK_STBY_EN_MASK                CommunicationTimer_TimerHW__PM_STBY_MSK

    /* Control Register Bit Locations */
    /* Interrupt Count - Not valid for Fixed Function Block */
    #define CommunicationTimer_CTRL_INTCNT_SHIFT                  0x00u
    /* Trigger Polarity - Not valid for Fixed Function Block */
    #define CommunicationTimer_CTRL_TRIG_MODE_SHIFT               0x00u
    /* Trigger Enable - Not valid for Fixed Function Block */
    #define CommunicationTimer_CTRL_TRIG_EN_SHIFT                 0x00u
    /* Capture Polarity - Not valid for Fixed Function Block */
    #define CommunicationTimer_CTRL_CAP_MODE_SHIFT                0x00u
    /* Timer Enable - As defined in Register Map, part of TMRX_CFG0 register */
    #define CommunicationTimer_CTRL_ENABLE_SHIFT                  0x00u

    /* Control Register Bit Masks */
    #define CommunicationTimer_CTRL_ENABLE                        ((uint8)((uint8)0x01u << CommunicationTimer_CTRL_ENABLE_SHIFT))

    /* Control2 Register Bit Masks */
    /* As defined in Register Map, Part of the TMRX_CFG1 register */
    #define CommunicationTimer_CTRL2_IRQ_SEL_SHIFT                 0x00u
    #define CommunicationTimer_CTRL2_IRQ_SEL                      ((uint8)((uint8)0x01u << CommunicationTimer_CTRL2_IRQ_SEL_SHIFT))

    #if (CY_PSOC5A)
        /* Use CFG1 Mode bits to set run mode */
        /* As defined by Verilog Implementation */
        #define CommunicationTimer_CTRL_MODE_SHIFT                 0x01u
        #define CommunicationTimer_CTRL_MODE_MASK                 ((uint8)((uint8)0x07u << CommunicationTimer_CTRL_MODE_SHIFT))
    #endif /* (CY_PSOC5A) */
    #if (CY_PSOC3 || CY_PSOC5LP)
        /* Control3 Register Bit Locations */
        #define CommunicationTimer_CTRL_RCOD_SHIFT        0x02u
        #define CommunicationTimer_CTRL_ENBL_SHIFT        0x00u
        #define CommunicationTimer_CTRL_MODE_SHIFT        0x00u

        /* Control3 Register Bit Masks */
        #define CommunicationTimer_CTRL_RCOD_MASK  ((uint8)((uint8)0x03u << CommunicationTimer_CTRL_RCOD_SHIFT)) /* ROD and COD bit masks */
        #define CommunicationTimer_CTRL_ENBL_MASK  ((uint8)((uint8)0x80u << CommunicationTimer_CTRL_ENBL_SHIFT)) /* HW_EN bit mask */
        #define CommunicationTimer_CTRL_MODE_MASK  ((uint8)((uint8)0x03u << CommunicationTimer_CTRL_MODE_SHIFT)) /* Run mode bit mask */

        #define CommunicationTimer_CTRL_RCOD       ((uint8)((uint8)0x03u << CommunicationTimer_CTRL_RCOD_SHIFT))
        #define CommunicationTimer_CTRL_ENBL       ((uint8)((uint8)0x80u << CommunicationTimer_CTRL_ENBL_SHIFT))
    #endif /* (CY_PSOC3 || CY_PSOC5LP) */

    /*RT1 Synch Constants: Applicable for PSoC3 and PSoC5LP */
    #define CommunicationTimer_RT1_SHIFT                       0x04u
    /* Sync TC and CMP bit masks */
    #define CommunicationTimer_RT1_MASK                        ((uint8)((uint8)0x03u << CommunicationTimer_RT1_SHIFT))
    #define CommunicationTimer_SYNC                            ((uint8)((uint8)0x03u << CommunicationTimer_RT1_SHIFT))
    #define CommunicationTimer_SYNCDSI_SHIFT                   0x00u
    /* Sync all DSI inputs with Mask  */
    #define CommunicationTimer_SYNCDSI_MASK                    ((uint8)((uint8)0x0Fu << CommunicationTimer_SYNCDSI_SHIFT))
    /* Sync all DSI inputs */
    #define CommunicationTimer_SYNCDSI_EN                      ((uint8)((uint8)0x0Fu << CommunicationTimer_SYNCDSI_SHIFT))

    #define CommunicationTimer_CTRL_MODE_PULSEWIDTH            ((uint8)((uint8)0x01u << CommunicationTimer_CTRL_MODE_SHIFT))
    #define CommunicationTimer_CTRL_MODE_PERIOD                ((uint8)((uint8)0x02u << CommunicationTimer_CTRL_MODE_SHIFT))
    #define CommunicationTimer_CTRL_MODE_CONTINUOUS            ((uint8)((uint8)0x00u << CommunicationTimer_CTRL_MODE_SHIFT))

    /* Status Register Bit Locations */
    /* As defined in Register Map, part of TMRX_SR0 register */
    #define CommunicationTimer_STATUS_TC_SHIFT                 0x07u
    /* As defined in Register Map, part of TMRX_SR0 register, Shared with Compare Status */
    #define CommunicationTimer_STATUS_CAPTURE_SHIFT            0x06u
    /* As defined in Register Map, part of TMRX_SR0 register */
    #define CommunicationTimer_STATUS_TC_INT_MASK_SHIFT        (CommunicationTimer_STATUS_TC_SHIFT - 0x04u)
    /* As defined in Register Map, part of TMRX_SR0 register, Shared with Compare Status */
    #define CommunicationTimer_STATUS_CAPTURE_INT_MASK_SHIFT   (CommunicationTimer_STATUS_CAPTURE_SHIFT - 0x04u)

    /* Status Register Bit Masks */
    #define CommunicationTimer_STATUS_TC                       ((uint8)((uint8)0x01u << CommunicationTimer_STATUS_TC_SHIFT))
    #define CommunicationTimer_STATUS_CAPTURE                  ((uint8)((uint8)0x01u << CommunicationTimer_STATUS_CAPTURE_SHIFT))
    /* Interrupt Enable Bit-Mask for interrupt on TC */
    #define CommunicationTimer_STATUS_TC_INT_MASK              ((uint8)((uint8)0x01u << CommunicationTimer_STATUS_TC_INT_MASK_SHIFT))
    /* Interrupt Enable Bit-Mask for interrupt on Capture */
    #define CommunicationTimer_STATUS_CAPTURE_INT_MASK         ((uint8)((uint8)0x01u << CommunicationTimer_STATUS_CAPTURE_INT_MASK_SHIFT))

#else   /* UDB Registers and Register Constants */


    /***************************************
    *           UDB Registers
    ***************************************/

    #define CommunicationTimer_STATUS              (* (reg8 *) CommunicationTimer_TimerUDB_rstSts_stsreg__STATUS_REG )
    #define CommunicationTimer_STATUS_MASK         (* (reg8 *) CommunicationTimer_TimerUDB_rstSts_stsreg__MASK_REG)
    #define CommunicationTimer_STATUS_AUX_CTRL     (* (reg8 *) CommunicationTimer_TimerUDB_rstSts_stsreg__STATUS_AUX_CTL_REG)
    #define CommunicationTimer_CONTROL             (* (reg8 *) CommunicationTimer_TimerUDB_sCTRLReg_SyncCtl_ctrlreg__CONTROL_REG )
    
    #if(CommunicationTimer_Resolution <= 8u) /* 8-bit Timer */
        #define CommunicationTimer_CAPTURE_LSB         (* (reg8 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__F0_REG )
        #define CommunicationTimer_CAPTURE_LSB_PTR       ((reg8 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__F0_REG )
        #define CommunicationTimer_PERIOD_LSB          (* (reg8 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__D0_REG )
        #define CommunicationTimer_PERIOD_LSB_PTR        ((reg8 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__D0_REG )
        #define CommunicationTimer_COUNTER_LSB         (* (reg8 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__A0_REG )
        #define CommunicationTimer_COUNTER_LSB_PTR       ((reg8 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__A0_REG )
    #elif(CommunicationTimer_Resolution <= 16u) /* 8-bit Timer */
        #if(CY_PSOC3) /* 8-bit addres space */
            #define CommunicationTimer_CAPTURE_LSB         (* (reg16 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__F0_REG )
            #define CommunicationTimer_CAPTURE_LSB_PTR       ((reg16 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__F0_REG )
            #define CommunicationTimer_PERIOD_LSB          (* (reg16 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__D0_REG )
            #define CommunicationTimer_PERIOD_LSB_PTR        ((reg16 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__D0_REG )
            #define CommunicationTimer_COUNTER_LSB         (* (reg16 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__A0_REG )
            #define CommunicationTimer_COUNTER_LSB_PTR       ((reg16 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__A0_REG )
        #else /* 16-bit address space */
            #define CommunicationTimer_CAPTURE_LSB         (* (reg16 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__16BIT_F0_REG )
            #define CommunicationTimer_CAPTURE_LSB_PTR       ((reg16 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__16BIT_F0_REG )
            #define CommunicationTimer_PERIOD_LSB          (* (reg16 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__16BIT_D0_REG )
            #define CommunicationTimer_PERIOD_LSB_PTR        ((reg16 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__16BIT_D0_REG )
            #define CommunicationTimer_COUNTER_LSB         (* (reg16 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__16BIT_A0_REG )
            #define CommunicationTimer_COUNTER_LSB_PTR       ((reg16 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__16BIT_A0_REG )
        #endif /* CY_PSOC3 */
    #elif(CommunicationTimer_Resolution <= 24u)/* 24-bit Timer */
        #define CommunicationTimer_CAPTURE_LSB         (* (reg32 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__F0_REG )
        #define CommunicationTimer_CAPTURE_LSB_PTR       ((reg32 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__F0_REG )
        #define CommunicationTimer_PERIOD_LSB          (* (reg32 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__D0_REG )
        #define CommunicationTimer_PERIOD_LSB_PTR        ((reg32 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__D0_REG )
        #define CommunicationTimer_COUNTER_LSB         (* (reg32 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__A0_REG )
        #define CommunicationTimer_COUNTER_LSB_PTR       ((reg32 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__A0_REG )
    #else /* 32-bit Timer */
        #if(CY_PSOC3 || CY_PSOC5) /* 8-bit address space */
            #define CommunicationTimer_CAPTURE_LSB         (* (reg32 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__F0_REG )
            #define CommunicationTimer_CAPTURE_LSB_PTR       ((reg32 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__F0_REG )
            #define CommunicationTimer_PERIOD_LSB          (* (reg32 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__D0_REG )
            #define CommunicationTimer_PERIOD_LSB_PTR        ((reg32 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__D0_REG )
            #define CommunicationTimer_COUNTER_LSB         (* (reg32 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__A0_REG )
            #define CommunicationTimer_COUNTER_LSB_PTR       ((reg32 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__A0_REG )
        #else /* 32-bit address space */
            #define CommunicationTimer_CAPTURE_LSB         (* (reg32 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__32BIT_F0_REG )
            #define CommunicationTimer_CAPTURE_LSB_PTR       ((reg32 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__32BIT_F0_REG )
            #define CommunicationTimer_PERIOD_LSB          (* (reg32 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__32BIT_D0_REG )
            #define CommunicationTimer_PERIOD_LSB_PTR        ((reg32 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__32BIT_D0_REG )
            #define CommunicationTimer_COUNTER_LSB         (* (reg32 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__32BIT_A0_REG )
            #define CommunicationTimer_COUNTER_LSB_PTR       ((reg32 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__32BIT_A0_REG )
        #endif /* CY_PSOC3 || CY_PSOC5 */ 
    #endif

    #define CommunicationTimer_COUNTER_LSB_PTR_8BIT       ((reg8 *) CommunicationTimer_TimerUDB_sT8_timerdp_u0__A0_REG )
    
    #if (CommunicationTimer_UsingHWCaptureCounter)
        #define CommunicationTimer_CAP_COUNT              (*(reg8 *) CommunicationTimer_TimerUDB_sCapCount_counter__PERIOD_REG )
        #define CommunicationTimer_CAP_COUNT_PTR          ( (reg8 *) CommunicationTimer_TimerUDB_sCapCount_counter__PERIOD_REG )
        #define CommunicationTimer_CAPTURE_COUNT_CTRL     (*(reg8 *) CommunicationTimer_TimerUDB_sCapCount_counter__CONTROL_AUX_CTL_REG )
        #define CommunicationTimer_CAPTURE_COUNT_CTRL_PTR ( (reg8 *) CommunicationTimer_TimerUDB_sCapCount_counter__CONTROL_AUX_CTL_REG )
    #endif /* (CommunicationTimer_UsingHWCaptureCounter) */


    /***************************************
    *       Register Constants
    ***************************************/

    /* Control Register Bit Locations */
    #define CommunicationTimer_CTRL_INTCNT_SHIFT              0x00u       /* As defined by Verilog Implementation */
    #define CommunicationTimer_CTRL_TRIG_MODE_SHIFT           0x02u       /* As defined by Verilog Implementation */
    #define CommunicationTimer_CTRL_TRIG_EN_SHIFT             0x04u       /* As defined by Verilog Implementation */
    #define CommunicationTimer_CTRL_CAP_MODE_SHIFT            0x05u       /* As defined by Verilog Implementation */
    #define CommunicationTimer_CTRL_ENABLE_SHIFT              0x07u       /* As defined by Verilog Implementation */

    /* Control Register Bit Masks */
    #define CommunicationTimer_CTRL_INTCNT_MASK               ((uint8)((uint8)0x03u << CommunicationTimer_CTRL_INTCNT_SHIFT))
    #define CommunicationTimer_CTRL_TRIG_MODE_MASK            ((uint8)((uint8)0x03u << CommunicationTimer_CTRL_TRIG_MODE_SHIFT))
    #define CommunicationTimer_CTRL_TRIG_EN                   ((uint8)((uint8)0x01u << CommunicationTimer_CTRL_TRIG_EN_SHIFT))
    #define CommunicationTimer_CTRL_CAP_MODE_MASK             ((uint8)((uint8)0x03u << CommunicationTimer_CTRL_CAP_MODE_SHIFT))
    #define CommunicationTimer_CTRL_ENABLE                    ((uint8)((uint8)0x01u << CommunicationTimer_CTRL_ENABLE_SHIFT))

    /* Bit Counter (7-bit) Control Register Bit Definitions */
    /* As defined by the Register map for the AUX Control Register */
    #define CommunicationTimer_CNTR_ENABLE                    0x20u

    /* Status Register Bit Locations */
    #define CommunicationTimer_STATUS_TC_SHIFT                0x00u  /* As defined by Verilog Implementation */
    #define CommunicationTimer_STATUS_CAPTURE_SHIFT           0x01u  /* As defined by Verilog Implementation */
    #define CommunicationTimer_STATUS_TC_INT_MASK_SHIFT       CommunicationTimer_STATUS_TC_SHIFT
    #define CommunicationTimer_STATUS_CAPTURE_INT_MASK_SHIFT  CommunicationTimer_STATUS_CAPTURE_SHIFT
    #define CommunicationTimer_STATUS_FIFOFULL_SHIFT          0x02u  /* As defined by Verilog Implementation */
    #define CommunicationTimer_STATUS_FIFONEMP_SHIFT          0x03u  /* As defined by Verilog Implementation */
    #define CommunicationTimer_STATUS_FIFOFULL_INT_MASK_SHIFT CommunicationTimer_STATUS_FIFOFULL_SHIFT

    /* Status Register Bit Masks */
    /* Sticky TC Event Bit-Mask */
    #define CommunicationTimer_STATUS_TC                      ((uint8)((uint8)0x01u << CommunicationTimer_STATUS_TC_SHIFT))
    /* Sticky Capture Event Bit-Mask */
    #define CommunicationTimer_STATUS_CAPTURE                 ((uint8)((uint8)0x01u << CommunicationTimer_STATUS_CAPTURE_SHIFT))
    /* Interrupt Enable Bit-Mask */
    #define CommunicationTimer_STATUS_TC_INT_MASK             ((uint8)((uint8)0x01u << CommunicationTimer_STATUS_TC_SHIFT))
    /* Interrupt Enable Bit-Mask */
    #define CommunicationTimer_STATUS_CAPTURE_INT_MASK        ((uint8)((uint8)0x01u << CommunicationTimer_STATUS_CAPTURE_SHIFT))
    /* NOT-Sticky FIFO Full Bit-Mask */
    #define CommunicationTimer_STATUS_FIFOFULL                ((uint8)((uint8)0x01u << CommunicationTimer_STATUS_FIFOFULL_SHIFT))
    /* NOT-Sticky FIFO Not Empty Bit-Mask */
    #define CommunicationTimer_STATUS_FIFONEMP                ((uint8)((uint8)0x01u << CommunicationTimer_STATUS_FIFONEMP_SHIFT))
    /* Interrupt Enable Bit-Mask */
    #define CommunicationTimer_STATUS_FIFOFULL_INT_MASK       ((uint8)((uint8)0x01u << CommunicationTimer_STATUS_FIFOFULL_SHIFT))

    #define CommunicationTimer_STATUS_ACTL_INT_EN             0x10u   /* As defined for the ACTL Register */

    /* Datapath Auxillary Control Register definitions */
    #define CommunicationTimer_AUX_CTRL_FIFO0_CLR             0x01u   /* As defined by Register map */
    #define CommunicationTimer_AUX_CTRL_FIFO1_CLR             0x02u   /* As defined by Register map */
    #define CommunicationTimer_AUX_CTRL_FIFO0_LVL             0x04u   /* As defined by Register map */
    #define CommunicationTimer_AUX_CTRL_FIFO1_LVL             0x08u   /* As defined by Register map */
    #define CommunicationTimer_STATUS_ACTL_INT_EN_MASK        0x10u   /* As defined for the ACTL Register */

#endif /* Implementation Specific Registers and Register Constants */

#endif  /* CY_TIMER_CommunicationTimer_H */


/* [] END OF FILE */
