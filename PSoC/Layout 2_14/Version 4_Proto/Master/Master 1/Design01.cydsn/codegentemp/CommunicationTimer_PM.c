/*******************************************************************************
* File Name: CommunicationTimer_PM.c
* Version 2.80
*
*  Description:
*     This file provides the power management source code to API for the
*     Timer.
*
*   Note:
*     None
*
*******************************************************************************
* Copyright 2008-2017, Cypress Semiconductor Corporation.  All rights reserved.
* You may use this file only in accordance with the license, terms, conditions,
* disclaimers, and limitations in the end user license agreement accompanying
* the software package with which this file was provided.
********************************************************************************/

#include "CommunicationTimer.h"

static CommunicationTimer_backupStruct CommunicationTimer_backup;


/*******************************************************************************
* Function Name: CommunicationTimer_SaveConfig
********************************************************************************
*
* Summary:
*     Save the current user configuration
*
* Parameters:
*  void
*
* Return:
*  void
*
* Global variables:
*  CommunicationTimer_backup:  Variables of this global structure are modified to
*  store the values of non retention configuration registers when Sleep() API is
*  called.
*
*******************************************************************************/
void CommunicationTimer_SaveConfig(void) 
{
    #if (!CommunicationTimer_UsingFixedFunction)
        CommunicationTimer_backup.TimerUdb = CommunicationTimer_ReadCounter();
        CommunicationTimer_backup.InterruptMaskValue = CommunicationTimer_STATUS_MASK;
        #if (CommunicationTimer_UsingHWCaptureCounter)
            CommunicationTimer_backup.TimerCaptureCounter = CommunicationTimer_ReadCaptureCount();
        #endif /* Back Up capture counter register  */

        #if(!CommunicationTimer_UDB_CONTROL_REG_REMOVED)
            CommunicationTimer_backup.TimerControlRegister = CommunicationTimer_ReadControlRegister();
        #endif /* Backup the enable state of the Timer component */
    #endif /* Backup non retention registers in UDB implementation. All fixed function registers are retention */
}


/*******************************************************************************
* Function Name: CommunicationTimer_RestoreConfig
********************************************************************************
*
* Summary:
*  Restores the current user configuration.
*
* Parameters:
*  void
*
* Return:
*  void
*
* Global variables:
*  CommunicationTimer_backup:  Variables of this global structure are used to
*  restore the values of non retention registers on wakeup from sleep mode.
*
*******************************************************************************/
void CommunicationTimer_RestoreConfig(void) 
{   
    #if (!CommunicationTimer_UsingFixedFunction)

        CommunicationTimer_WriteCounter(CommunicationTimer_backup.TimerUdb);
        CommunicationTimer_STATUS_MASK =CommunicationTimer_backup.InterruptMaskValue;
        #if (CommunicationTimer_UsingHWCaptureCounter)
            CommunicationTimer_SetCaptureCount(CommunicationTimer_backup.TimerCaptureCounter);
        #endif /* Restore Capture counter register*/

        #if(!CommunicationTimer_UDB_CONTROL_REG_REMOVED)
            CommunicationTimer_WriteControlRegister(CommunicationTimer_backup.TimerControlRegister);
        #endif /* Restore the enable state of the Timer component */
    #endif /* Restore non retention registers in the UDB implementation only */
}


/*******************************************************************************
* Function Name: CommunicationTimer_Sleep
********************************************************************************
*
* Summary:
*     Stop and Save the user configuration
*
* Parameters:
*  void
*
* Return:
*  void
*
* Global variables:
*  CommunicationTimer_backup.TimerEnableState:  Is modified depending on the
*  enable state of the block before entering sleep mode.
*
*******************************************************************************/
void CommunicationTimer_Sleep(void) 
{
    #if(!CommunicationTimer_UDB_CONTROL_REG_REMOVED)
        /* Save Counter's enable state */
        if(CommunicationTimer_CTRL_ENABLE == (CommunicationTimer_CONTROL & CommunicationTimer_CTRL_ENABLE))
        {
            /* Timer is enabled */
            CommunicationTimer_backup.TimerEnableState = 1u;
        }
        else
        {
            /* Timer is disabled */
            CommunicationTimer_backup.TimerEnableState = 0u;
        }
    #endif /* Back up enable state from the Timer control register */
    CommunicationTimer_Stop();
    CommunicationTimer_SaveConfig();
}


/*******************************************************************************
* Function Name: CommunicationTimer_Wakeup
********************************************************************************
*
* Summary:
*  Restores and enables the user configuration
*
* Parameters:
*  void
*
* Return:
*  void
*
* Global variables:
*  CommunicationTimer_backup.enableState:  Is used to restore the enable state of
*  block on wakeup from sleep mode.
*
*******************************************************************************/
void CommunicationTimer_Wakeup(void) 
{
    CommunicationTimer_RestoreConfig();
    #if(!CommunicationTimer_UDB_CONTROL_REG_REMOVED)
        if(CommunicationTimer_backup.TimerEnableState == 1u)
        {     /* Enable Timer's operation */
                CommunicationTimer_Enable();
        } /* Do nothing if Timer was disabled before */
    #endif /* Remove this code section if Control register is removed */
}


/* [] END OF FILE */
