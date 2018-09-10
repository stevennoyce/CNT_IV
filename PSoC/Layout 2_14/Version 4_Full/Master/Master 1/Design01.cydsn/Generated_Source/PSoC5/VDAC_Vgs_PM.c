/*******************************************************************************
* File Name: VDAC_Vgs_PM.c  
* Version 1.90
*
* Description:
*  This file provides the power management source code to API for the
*  VDAC8.  
*
* Note:
*  None
*
********************************************************************************
* Copyright 2008-2012, Cypress Semiconductor Corporation.  All rights reserved.
* You may use this file only in accordance with the license, terms, conditions, 
* disclaimers, and limitations in the end user license agreement accompanying 
* the software package with which this file was provided.
*******************************************************************************/

#include "VDAC_Vgs.h"

static VDAC_Vgs_backupStruct VDAC_Vgs_backup;


/*******************************************************************************
* Function Name: VDAC_Vgs_SaveConfig
********************************************************************************
* Summary:
*  Save the current user configuration
*
* Parameters:  
*  void  
*
* Return: 
*  void
*
*******************************************************************************/
void VDAC_Vgs_SaveConfig(void) 
{
    if (!((VDAC_Vgs_CR1 & VDAC_Vgs_SRC_MASK) == VDAC_Vgs_SRC_UDB))
    {
        VDAC_Vgs_backup.data_value = VDAC_Vgs_Data;
    }
}


/*******************************************************************************
* Function Name: VDAC_Vgs_RestoreConfig
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
*******************************************************************************/
void VDAC_Vgs_RestoreConfig(void) 
{
    if (!((VDAC_Vgs_CR1 & VDAC_Vgs_SRC_MASK) == VDAC_Vgs_SRC_UDB))
    {
        if((VDAC_Vgs_Strobe & VDAC_Vgs_STRB_MASK) == VDAC_Vgs_STRB_EN)
        {
            VDAC_Vgs_Strobe &= (uint8)(~VDAC_Vgs_STRB_MASK);
            VDAC_Vgs_Data = VDAC_Vgs_backup.data_value;
            VDAC_Vgs_Strobe |= VDAC_Vgs_STRB_EN;
        }
        else
        {
            VDAC_Vgs_Data = VDAC_Vgs_backup.data_value;
        }
    }
}


/*******************************************************************************
* Function Name: VDAC_Vgs_Sleep
********************************************************************************
* Summary:
*  Stop and Save the user configuration
*
* Parameters:  
*  void:  
*
* Return: 
*  void
*
* Global variables:
*  VDAC_Vgs_backup.enableState:  Is modified depending on the enable 
*  state  of the block before entering sleep mode.
*
*******************************************************************************/
void VDAC_Vgs_Sleep(void) 
{
    /* Save VDAC8's enable state */    
    if(VDAC_Vgs_ACT_PWR_EN == (VDAC_Vgs_PWRMGR & VDAC_Vgs_ACT_PWR_EN))
    {
        /* VDAC8 is enabled */
        VDAC_Vgs_backup.enableState = 1u;
    }
    else
    {
        /* VDAC8 is disabled */
        VDAC_Vgs_backup.enableState = 0u;
    }
    
    VDAC_Vgs_Stop();
    VDAC_Vgs_SaveConfig();
}


/*******************************************************************************
* Function Name: VDAC_Vgs_Wakeup
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
*  VDAC_Vgs_backup.enableState:  Is used to restore the enable state of 
*  block on wakeup from sleep mode.
*
*******************************************************************************/
void VDAC_Vgs_Wakeup(void) 
{
    VDAC_Vgs_RestoreConfig();
    
    if(VDAC_Vgs_backup.enableState == 1u)
    {
        /* Enable VDAC8's operation */
        VDAC_Vgs_Enable();

        /* Restore the data register */
        VDAC_Vgs_SetValue(VDAC_Vgs_Data);
    } /* Do nothing if VDAC8 was disabled before */    
}


/* [] END OF FILE */
