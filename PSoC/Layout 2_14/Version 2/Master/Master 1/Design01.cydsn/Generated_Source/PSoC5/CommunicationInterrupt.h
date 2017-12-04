/*******************************************************************************
* File Name: CommunicationInterrupt.h
* Version 1.70
*
*  Description:
*   Provides the function definitions for the Interrupt Controller.
*
*
********************************************************************************
* Copyright 2008-2015, Cypress Semiconductor Corporation.  All rights reserved.
* You may use this file only in accordance with the license, terms, conditions, 
* disclaimers, and limitations in the end user license agreement accompanying 
* the software package with which this file was provided.
*******************************************************************************/
#if !defined(CY_ISR_CommunicationInterrupt_H)
#define CY_ISR_CommunicationInterrupt_H


#include <cytypes.h>
#include <cyfitter.h>

/* Interrupt Controller API. */
void CommunicationInterrupt_Start(void);
void CommunicationInterrupt_StartEx(cyisraddress address);
void CommunicationInterrupt_Stop(void);

CY_ISR_PROTO(CommunicationInterrupt_Interrupt);

void CommunicationInterrupt_SetVector(cyisraddress address);
cyisraddress CommunicationInterrupt_GetVector(void);

void CommunicationInterrupt_SetPriority(uint8 priority);
uint8 CommunicationInterrupt_GetPriority(void);

void CommunicationInterrupt_Enable(void);
uint8 CommunicationInterrupt_GetState(void);
void CommunicationInterrupt_Disable(void);

void CommunicationInterrupt_SetPending(void);
void CommunicationInterrupt_ClearPending(void);


/* Interrupt Controller Constants */

/* Address of the INTC.VECT[x] register that contains the Address of the CommunicationInterrupt ISR. */
#define CommunicationInterrupt_INTC_VECTOR            ((reg32 *) CommunicationInterrupt__INTC_VECT)

/* Address of the CommunicationInterrupt ISR priority. */
#define CommunicationInterrupt_INTC_PRIOR             ((reg8 *) CommunicationInterrupt__INTC_PRIOR_REG)

/* Priority of the CommunicationInterrupt interrupt. */
#define CommunicationInterrupt_INTC_PRIOR_NUMBER      CommunicationInterrupt__INTC_PRIOR_NUM

/* Address of the INTC.SET_EN[x] byte to bit enable CommunicationInterrupt interrupt. */
#define CommunicationInterrupt_INTC_SET_EN            ((reg32 *) CommunicationInterrupt__INTC_SET_EN_REG)

/* Address of the INTC.CLR_EN[x] register to bit clear the CommunicationInterrupt interrupt. */
#define CommunicationInterrupt_INTC_CLR_EN            ((reg32 *) CommunicationInterrupt__INTC_CLR_EN_REG)

/* Address of the INTC.SET_PD[x] register to set the CommunicationInterrupt interrupt state to pending. */
#define CommunicationInterrupt_INTC_SET_PD            ((reg32 *) CommunicationInterrupt__INTC_SET_PD_REG)

/* Address of the INTC.CLR_PD[x] register to clear the CommunicationInterrupt interrupt. */
#define CommunicationInterrupt_INTC_CLR_PD            ((reg32 *) CommunicationInterrupt__INTC_CLR_PD_REG)


#endif /* CY_ISR_CommunicationInterrupt_H */


/* [] END OF FILE */
