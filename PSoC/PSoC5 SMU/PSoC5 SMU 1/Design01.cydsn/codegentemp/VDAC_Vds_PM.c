/*******************************************************************************
* File Name: VDAC_Vds_PM.c  
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

#include "VDAC_Vds.h"

static VDAC_Vds_backupStruct VDAC_Vds_backup;


/*******************************************************************************
* Function Name: VDAC_Vds_SaveConfig
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
void VDAC_Vds_SaveConfig(void) 
{
    if (!((VDAC_Vds_CR1 & VDAC_Vds_SRC_MASK) == VDAC_Vds_SRC_UDB))
    {
        VDAC_Vds_backup.data_value = VDAC_Vds_Data;
    }
}


/*******************************************************************************
* Function Name: VDAC_Vds_RestoreConfig
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
void VDAC_Vds_RestoreConfig(void) 
{
    if (!((VDAC_Vds_CR1 & VDAC_Vds_SRC_MASK) == VDAC_Vds_SRC_UDB))
    {
        if((VDAC_Vds_Strobe & VDAC_Vds_STRB_MASK) == VDAC_Vds_STRB_EN)
        {
            VDAC_Vds_Strobe &= (uint8)(~VDAC_Vds_STRB_MASK);
            VDAC_Vds_Data = VDAC_Vds_backup.data_value;
            VDAC_Vds_Strobe |= VDAC_Vds_STRB_EN;
        }
        else
        {
            VDAC_Vds_Data = VDAC_Vds_backup.data_value;
        }
    }
}


/*******************************************************************************
* Function Name: VDAC_Vds_Sleep
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
*  VDAC_Vds_backup.enableState:  Is modified depending on the enable 
*  state  of the block before entering sleep mode.
*
*******************************************************************************/
void VDAC_Vds_Sleep(void) 
{
    /* Save VDAC8's enable state */    
    if(VDAC_Vds_ACT_PWR_EN == (VDAC_Vds_PWRMGR & VDAC_Vds_ACT_PWR_EN))
    {
        /* VDAC8 is enabled */
        VDAC_Vds_backup.enableState = 1u;
    }
    else
    {
        /* VDAC8 is disabled */
        VDAC_Vds_backup.enableState = 0u;
    }
    
    VDAC_Vds_Stop();
    VDAC_Vds_SaveConfig();
}


/*******************************************************************************
* Function Name: VDAC_Vds_Wakeup
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
*  VDAC_Vds_backup.enableState:  Is used to restore the enable state of 
*  block on wakeup from sleep mode.
*
*******************************************************************************/
void VDAC_Vds_Wakeup(void) 
{
    VDAC_Vds_RestoreConfig();
    
    if(VDAC_Vds_backup.enableState == 1u)
    {
        /* Enable VDAC8's operation */
        VDAC_Vds_Enable();

        /* Restore the data register */
        VDAC_Vds_SetValue(VDAC_Vds_Data);
    } /* Do nothing if VDAC8 was disabled before */    
}


/* [] END OF FILE */
