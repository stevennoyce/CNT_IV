/*******************************************************************************
* File Name: cyfitter.h
* 
* PSoC Creator  4.1 Update 1
*
* Description:
* 
* This file is automatically generated by PSoC Creator.
*
********************************************************************************
* Copyright (c) 2007-2017 Cypress Semiconductor.  All rights reserved.
* You may use this file only in accordance with the license, terms, conditions, 
* disclaimers, and limitations in the end user license agreement accompanying 
* the software package with which this file was provided.
********************************************************************************/

#ifndef INCLUDED_CYFITTER_H
#define INCLUDED_CYFITTER_H
#include "cydevice_trm.h"

/* Button */
#define Button__0__DM__MASK 0xE00000u
#define Button__0__DM__SHIFT 21u
#define Button__0__DR CYREG_PRT0_DR
#define Button__0__HSIOM CYREG_HSIOM_PORT_SEL0
#define Button__0__HSIOM_MASK 0xF0000000u
#define Button__0__HSIOM_SHIFT 28u
#define Button__0__INTCFG CYREG_PRT0_INTCFG
#define Button__0__INTSTAT CYREG_PRT0_INTSTAT
#define Button__0__MASK 0x80u
#define Button__0__PA__CFG0 CYREG_UDB_PA0_CFG0
#define Button__0__PA__CFG1 CYREG_UDB_PA0_CFG1
#define Button__0__PA__CFG10 CYREG_UDB_PA0_CFG10
#define Button__0__PA__CFG11 CYREG_UDB_PA0_CFG11
#define Button__0__PA__CFG12 CYREG_UDB_PA0_CFG12
#define Button__0__PA__CFG13 CYREG_UDB_PA0_CFG13
#define Button__0__PA__CFG14 CYREG_UDB_PA0_CFG14
#define Button__0__PA__CFG2 CYREG_UDB_PA0_CFG2
#define Button__0__PA__CFG3 CYREG_UDB_PA0_CFG3
#define Button__0__PA__CFG4 CYREG_UDB_PA0_CFG4
#define Button__0__PA__CFG5 CYREG_UDB_PA0_CFG5
#define Button__0__PA__CFG6 CYREG_UDB_PA0_CFG6
#define Button__0__PA__CFG7 CYREG_UDB_PA0_CFG7
#define Button__0__PA__CFG8 CYREG_UDB_PA0_CFG8
#define Button__0__PA__CFG9 CYREG_UDB_PA0_CFG9
#define Button__0__PC CYREG_PRT0_PC
#define Button__0__PC2 CYREG_PRT0_PC2
#define Button__0__PORT 0u
#define Button__0__PS CYREG_PRT0_PS
#define Button__0__SHIFT 7u
#define Button__DR CYREG_PRT0_DR
#define Button__INTCFG CYREG_PRT0_INTCFG
#define Button__INTSTAT CYREG_PRT0_INTSTAT
#define Button__MASK 0x80u
#define Button__PA__CFG0 CYREG_UDB_PA0_CFG0
#define Button__PA__CFG1 CYREG_UDB_PA0_CFG1
#define Button__PA__CFG10 CYREG_UDB_PA0_CFG10
#define Button__PA__CFG11 CYREG_UDB_PA0_CFG11
#define Button__PA__CFG12 CYREG_UDB_PA0_CFG12
#define Button__PA__CFG13 CYREG_UDB_PA0_CFG13
#define Button__PA__CFG14 CYREG_UDB_PA0_CFG14
#define Button__PA__CFG2 CYREG_UDB_PA0_CFG2
#define Button__PA__CFG3 CYREG_UDB_PA0_CFG3
#define Button__PA__CFG4 CYREG_UDB_PA0_CFG4
#define Button__PA__CFG5 CYREG_UDB_PA0_CFG5
#define Button__PA__CFG6 CYREG_UDB_PA0_CFG6
#define Button__PA__CFG7 CYREG_UDB_PA0_CFG7
#define Button__PA__CFG8 CYREG_UDB_PA0_CFG8
#define Button__PA__CFG9 CYREG_UDB_PA0_CFG9
#define Button__PC CYREG_PRT0_PC
#define Button__PC2 CYREG_PRT0_PC2
#define Button__PORT 0u
#define Button__PS CYREG_PRT0_PS
#define Button__SHIFT 7u

/* EZI2C_1 */
#define EZI2C_1_SCB__BIST_CONTROL CYREG_SCB1_BIST_CONTROL
#define EZI2C_1_SCB__BIST_DATA CYREG_SCB1_BIST_DATA
#define EZI2C_1_SCB__CTRL CYREG_SCB1_CTRL
#define EZI2C_1_SCB__EZ_DATA00 CYREG_SCB1_EZ_DATA00
#define EZI2C_1_SCB__EZ_DATA01 CYREG_SCB1_EZ_DATA01
#define EZI2C_1_SCB__EZ_DATA02 CYREG_SCB1_EZ_DATA02
#define EZI2C_1_SCB__EZ_DATA03 CYREG_SCB1_EZ_DATA03
#define EZI2C_1_SCB__EZ_DATA04 CYREG_SCB1_EZ_DATA04
#define EZI2C_1_SCB__EZ_DATA05 CYREG_SCB1_EZ_DATA05
#define EZI2C_1_SCB__EZ_DATA06 CYREG_SCB1_EZ_DATA06
#define EZI2C_1_SCB__EZ_DATA07 CYREG_SCB1_EZ_DATA07
#define EZI2C_1_SCB__EZ_DATA08 CYREG_SCB1_EZ_DATA08
#define EZI2C_1_SCB__EZ_DATA09 CYREG_SCB1_EZ_DATA09
#define EZI2C_1_SCB__EZ_DATA10 CYREG_SCB1_EZ_DATA10
#define EZI2C_1_SCB__EZ_DATA11 CYREG_SCB1_EZ_DATA11
#define EZI2C_1_SCB__EZ_DATA12 CYREG_SCB1_EZ_DATA12
#define EZI2C_1_SCB__EZ_DATA13 CYREG_SCB1_EZ_DATA13
#define EZI2C_1_SCB__EZ_DATA14 CYREG_SCB1_EZ_DATA14
#define EZI2C_1_SCB__EZ_DATA15 CYREG_SCB1_EZ_DATA15
#define EZI2C_1_SCB__EZ_DATA16 CYREG_SCB1_EZ_DATA16
#define EZI2C_1_SCB__EZ_DATA17 CYREG_SCB1_EZ_DATA17
#define EZI2C_1_SCB__EZ_DATA18 CYREG_SCB1_EZ_DATA18
#define EZI2C_1_SCB__EZ_DATA19 CYREG_SCB1_EZ_DATA19
#define EZI2C_1_SCB__EZ_DATA20 CYREG_SCB1_EZ_DATA20
#define EZI2C_1_SCB__EZ_DATA21 CYREG_SCB1_EZ_DATA21
#define EZI2C_1_SCB__EZ_DATA22 CYREG_SCB1_EZ_DATA22
#define EZI2C_1_SCB__EZ_DATA23 CYREG_SCB1_EZ_DATA23
#define EZI2C_1_SCB__EZ_DATA24 CYREG_SCB1_EZ_DATA24
#define EZI2C_1_SCB__EZ_DATA25 CYREG_SCB1_EZ_DATA25
#define EZI2C_1_SCB__EZ_DATA26 CYREG_SCB1_EZ_DATA26
#define EZI2C_1_SCB__EZ_DATA27 CYREG_SCB1_EZ_DATA27
#define EZI2C_1_SCB__EZ_DATA28 CYREG_SCB1_EZ_DATA28
#define EZI2C_1_SCB__EZ_DATA29 CYREG_SCB1_EZ_DATA29
#define EZI2C_1_SCB__EZ_DATA30 CYREG_SCB1_EZ_DATA30
#define EZI2C_1_SCB__EZ_DATA31 CYREG_SCB1_EZ_DATA31
#define EZI2C_1_SCB__I2C_CFG CYREG_SCB1_I2C_CFG
#define EZI2C_1_SCB__I2C_CTRL CYREG_SCB1_I2C_CTRL
#define EZI2C_1_SCB__I2C_M_CMD CYREG_SCB1_I2C_M_CMD
#define EZI2C_1_SCB__I2C_S_CMD CYREG_SCB1_I2C_S_CMD
#define EZI2C_1_SCB__I2C_STATUS CYREG_SCB1_I2C_STATUS
#define EZI2C_1_SCB__INTR_CAUSE CYREG_SCB1_INTR_CAUSE
#define EZI2C_1_SCB__INTR_I2C_EC CYREG_SCB1_INTR_I2C_EC
#define EZI2C_1_SCB__INTR_I2C_EC_MASK CYREG_SCB1_INTR_I2C_EC_MASK
#define EZI2C_1_SCB__INTR_I2C_EC_MASKED CYREG_SCB1_INTR_I2C_EC_MASKED
#define EZI2C_1_SCB__INTR_M CYREG_SCB1_INTR_M
#define EZI2C_1_SCB__INTR_M_MASK CYREG_SCB1_INTR_M_MASK
#define EZI2C_1_SCB__INTR_M_MASKED CYREG_SCB1_INTR_M_MASKED
#define EZI2C_1_SCB__INTR_M_SET CYREG_SCB1_INTR_M_SET
#define EZI2C_1_SCB__INTR_RX CYREG_SCB1_INTR_RX
#define EZI2C_1_SCB__INTR_RX_MASK CYREG_SCB1_INTR_RX_MASK
#define EZI2C_1_SCB__INTR_RX_MASKED CYREG_SCB1_INTR_RX_MASKED
#define EZI2C_1_SCB__INTR_RX_SET CYREG_SCB1_INTR_RX_SET
#define EZI2C_1_SCB__INTR_S CYREG_SCB1_INTR_S
#define EZI2C_1_SCB__INTR_S_MASK CYREG_SCB1_INTR_S_MASK
#define EZI2C_1_SCB__INTR_S_MASKED CYREG_SCB1_INTR_S_MASKED
#define EZI2C_1_SCB__INTR_S_SET CYREG_SCB1_INTR_S_SET
#define EZI2C_1_SCB__INTR_SPI_EC CYREG_SCB1_INTR_SPI_EC
#define EZI2C_1_SCB__INTR_SPI_EC_MASK CYREG_SCB1_INTR_SPI_EC_MASK
#define EZI2C_1_SCB__INTR_SPI_EC_MASKED CYREG_SCB1_INTR_SPI_EC_MASKED
#define EZI2C_1_SCB__INTR_TX CYREG_SCB1_INTR_TX
#define EZI2C_1_SCB__INTR_TX_MASK CYREG_SCB1_INTR_TX_MASK
#define EZI2C_1_SCB__INTR_TX_MASKED CYREG_SCB1_INTR_TX_MASKED
#define EZI2C_1_SCB__INTR_TX_SET CYREG_SCB1_INTR_TX_SET
#define EZI2C_1_SCB__RX_CTRL CYREG_SCB1_RX_CTRL
#define EZI2C_1_SCB__RX_FIFO_CTRL CYREG_SCB1_RX_FIFO_CTRL
#define EZI2C_1_SCB__RX_FIFO_RD CYREG_SCB1_RX_FIFO_RD
#define EZI2C_1_SCB__RX_FIFO_RD_SILENT CYREG_SCB1_RX_FIFO_RD_SILENT
#define EZI2C_1_SCB__RX_FIFO_STATUS CYREG_SCB1_RX_FIFO_STATUS
#define EZI2C_1_SCB__RX_MATCH CYREG_SCB1_RX_MATCH
#define EZI2C_1_SCB__SPI_CTRL CYREG_SCB1_SPI_CTRL
#define EZI2C_1_SCB__SPI_STATUS CYREG_SCB1_SPI_STATUS
#define EZI2C_1_SCB__SS0_POSISTION 0u
#define EZI2C_1_SCB__SS1_POSISTION 1u
#define EZI2C_1_SCB__SS2_POSISTION 2u
#define EZI2C_1_SCB__SS3_POSISTION 3u
#define EZI2C_1_SCB__STATUS CYREG_SCB1_STATUS
#define EZI2C_1_SCB__TX_CTRL CYREG_SCB1_TX_CTRL
#define EZI2C_1_SCB__TX_FIFO_CTRL CYREG_SCB1_TX_FIFO_CTRL
#define EZI2C_1_SCB__TX_FIFO_STATUS CYREG_SCB1_TX_FIFO_STATUS
#define EZI2C_1_SCB__TX_FIFO_WR CYREG_SCB1_TX_FIFO_WR
#define EZI2C_1_SCB__UART_CTRL CYREG_SCB1_UART_CTRL
#define EZI2C_1_SCB__UART_RX_CTRL CYREG_SCB1_UART_RX_CTRL
#define EZI2C_1_SCB__UART_RX_STATUS CYREG_SCB1_UART_RX_STATUS
#define EZI2C_1_SCB__UART_TX_CTRL CYREG_SCB1_UART_TX_CTRL
#define EZI2C_1_SCB_IRQ__INTC_CLR_EN_REG CYREG_CM0_ICER
#define EZI2C_1_SCB_IRQ__INTC_CLR_PD_REG CYREG_CM0_ICPR
#define EZI2C_1_SCB_IRQ__INTC_MASK 0x800u
#define EZI2C_1_SCB_IRQ__INTC_NUMBER 11u
#define EZI2C_1_SCB_IRQ__INTC_PRIOR_MASK 0xC0000000u
#define EZI2C_1_SCB_IRQ__INTC_PRIOR_NUM 3u
#define EZI2C_1_SCB_IRQ__INTC_PRIOR_REG CYREG_CM0_IPR2
#define EZI2C_1_SCB_IRQ__INTC_SET_EN_REG CYREG_CM0_ISER
#define EZI2C_1_SCB_IRQ__INTC_SET_PD_REG CYREG_CM0_ISPR
#define EZI2C_1_SCBCLK__DIVIDER_MASK 0x0000FFFFu
#define EZI2C_1_SCBCLK__ENABLE CYREG_CLK_DIVIDER_A00
#define EZI2C_1_SCBCLK__ENABLE_MASK 0x80000000u
#define EZI2C_1_SCBCLK__MASK 0x80000000u
#define EZI2C_1_SCBCLK__REGISTER CYREG_CLK_DIVIDER_A00
#define EZI2C_1_scl__0__DM__MASK 0x07u
#define EZI2C_1_scl__0__DM__SHIFT 0u
#define EZI2C_1_scl__0__DR CYREG_PRT3_DR
#define EZI2C_1_scl__0__HSIOM CYREG_HSIOM_PORT_SEL3
#define EZI2C_1_scl__0__HSIOM_GPIO 0u
#define EZI2C_1_scl__0__HSIOM_I2C 14u
#define EZI2C_1_scl__0__HSIOM_I2C_SCL 14u
#define EZI2C_1_scl__0__HSIOM_MASK 0x0000000Fu
#define EZI2C_1_scl__0__HSIOM_SHIFT 0u
#define EZI2C_1_scl__0__HSIOM_SPI 15u
#define EZI2C_1_scl__0__HSIOM_SPI_MOSI 15u
#define EZI2C_1_scl__0__HSIOM_UART 9u
#define EZI2C_1_scl__0__HSIOM_UART_RX 9u
#define EZI2C_1_scl__0__INTCFG CYREG_PRT3_INTCFG
#define EZI2C_1_scl__0__INTSTAT CYREG_PRT3_INTSTAT
#define EZI2C_1_scl__0__MASK 0x01u
#define EZI2C_1_scl__0__PA__CFG0 CYREG_UDB_PA3_CFG0
#define EZI2C_1_scl__0__PA__CFG1 CYREG_UDB_PA3_CFG1
#define EZI2C_1_scl__0__PA__CFG10 CYREG_UDB_PA3_CFG10
#define EZI2C_1_scl__0__PA__CFG11 CYREG_UDB_PA3_CFG11
#define EZI2C_1_scl__0__PA__CFG12 CYREG_UDB_PA3_CFG12
#define EZI2C_1_scl__0__PA__CFG13 CYREG_UDB_PA3_CFG13
#define EZI2C_1_scl__0__PA__CFG14 CYREG_UDB_PA3_CFG14
#define EZI2C_1_scl__0__PA__CFG2 CYREG_UDB_PA3_CFG2
#define EZI2C_1_scl__0__PA__CFG3 CYREG_UDB_PA3_CFG3
#define EZI2C_1_scl__0__PA__CFG4 CYREG_UDB_PA3_CFG4
#define EZI2C_1_scl__0__PA__CFG5 CYREG_UDB_PA3_CFG5
#define EZI2C_1_scl__0__PA__CFG6 CYREG_UDB_PA3_CFG6
#define EZI2C_1_scl__0__PA__CFG7 CYREG_UDB_PA3_CFG7
#define EZI2C_1_scl__0__PA__CFG8 CYREG_UDB_PA3_CFG8
#define EZI2C_1_scl__0__PA__CFG9 CYREG_UDB_PA3_CFG9
#define EZI2C_1_scl__0__PC CYREG_PRT3_PC
#define EZI2C_1_scl__0__PC2 CYREG_PRT3_PC2
#define EZI2C_1_scl__0__PORT 3u
#define EZI2C_1_scl__0__PS CYREG_PRT3_PS
#define EZI2C_1_scl__0__SHIFT 0u
#define EZI2C_1_scl__DR CYREG_PRT3_DR
#define EZI2C_1_scl__INTCFG CYREG_PRT3_INTCFG
#define EZI2C_1_scl__INTSTAT CYREG_PRT3_INTSTAT
#define EZI2C_1_scl__MASK 0x01u
#define EZI2C_1_scl__PA__CFG0 CYREG_UDB_PA3_CFG0
#define EZI2C_1_scl__PA__CFG1 CYREG_UDB_PA3_CFG1
#define EZI2C_1_scl__PA__CFG10 CYREG_UDB_PA3_CFG10
#define EZI2C_1_scl__PA__CFG11 CYREG_UDB_PA3_CFG11
#define EZI2C_1_scl__PA__CFG12 CYREG_UDB_PA3_CFG12
#define EZI2C_1_scl__PA__CFG13 CYREG_UDB_PA3_CFG13
#define EZI2C_1_scl__PA__CFG14 CYREG_UDB_PA3_CFG14
#define EZI2C_1_scl__PA__CFG2 CYREG_UDB_PA3_CFG2
#define EZI2C_1_scl__PA__CFG3 CYREG_UDB_PA3_CFG3
#define EZI2C_1_scl__PA__CFG4 CYREG_UDB_PA3_CFG4
#define EZI2C_1_scl__PA__CFG5 CYREG_UDB_PA3_CFG5
#define EZI2C_1_scl__PA__CFG6 CYREG_UDB_PA3_CFG6
#define EZI2C_1_scl__PA__CFG7 CYREG_UDB_PA3_CFG7
#define EZI2C_1_scl__PA__CFG8 CYREG_UDB_PA3_CFG8
#define EZI2C_1_scl__PA__CFG9 CYREG_UDB_PA3_CFG9
#define EZI2C_1_scl__PC CYREG_PRT3_PC
#define EZI2C_1_scl__PC2 CYREG_PRT3_PC2
#define EZI2C_1_scl__PORT 3u
#define EZI2C_1_scl__PS CYREG_PRT3_PS
#define EZI2C_1_scl__SHIFT 0u
#define EZI2C_1_sda__0__DM__MASK 0x38u
#define EZI2C_1_sda__0__DM__SHIFT 3u
#define EZI2C_1_sda__0__DR CYREG_PRT3_DR
#define EZI2C_1_sda__0__HSIOM CYREG_HSIOM_PORT_SEL3
#define EZI2C_1_sda__0__HSIOM_GPIO 0u
#define EZI2C_1_sda__0__HSIOM_I2C 14u
#define EZI2C_1_sda__0__HSIOM_I2C_SDA 14u
#define EZI2C_1_sda__0__HSIOM_MASK 0x000000F0u
#define EZI2C_1_sda__0__HSIOM_SHIFT 4u
#define EZI2C_1_sda__0__HSIOM_SPI 15u
#define EZI2C_1_sda__0__HSIOM_SPI_MISO 15u
#define EZI2C_1_sda__0__HSIOM_UART 9u
#define EZI2C_1_sda__0__HSIOM_UART_TX 9u
#define EZI2C_1_sda__0__INTCFG CYREG_PRT3_INTCFG
#define EZI2C_1_sda__0__INTSTAT CYREG_PRT3_INTSTAT
#define EZI2C_1_sda__0__MASK 0x02u
#define EZI2C_1_sda__0__PA__CFG0 CYREG_UDB_PA3_CFG0
#define EZI2C_1_sda__0__PA__CFG1 CYREG_UDB_PA3_CFG1
#define EZI2C_1_sda__0__PA__CFG10 CYREG_UDB_PA3_CFG10
#define EZI2C_1_sda__0__PA__CFG11 CYREG_UDB_PA3_CFG11
#define EZI2C_1_sda__0__PA__CFG12 CYREG_UDB_PA3_CFG12
#define EZI2C_1_sda__0__PA__CFG13 CYREG_UDB_PA3_CFG13
#define EZI2C_1_sda__0__PA__CFG14 CYREG_UDB_PA3_CFG14
#define EZI2C_1_sda__0__PA__CFG2 CYREG_UDB_PA3_CFG2
#define EZI2C_1_sda__0__PA__CFG3 CYREG_UDB_PA3_CFG3
#define EZI2C_1_sda__0__PA__CFG4 CYREG_UDB_PA3_CFG4
#define EZI2C_1_sda__0__PA__CFG5 CYREG_UDB_PA3_CFG5
#define EZI2C_1_sda__0__PA__CFG6 CYREG_UDB_PA3_CFG6
#define EZI2C_1_sda__0__PA__CFG7 CYREG_UDB_PA3_CFG7
#define EZI2C_1_sda__0__PA__CFG8 CYREG_UDB_PA3_CFG8
#define EZI2C_1_sda__0__PA__CFG9 CYREG_UDB_PA3_CFG9
#define EZI2C_1_sda__0__PC CYREG_PRT3_PC
#define EZI2C_1_sda__0__PC2 CYREG_PRT3_PC2
#define EZI2C_1_sda__0__PORT 3u
#define EZI2C_1_sda__0__PS CYREG_PRT3_PS
#define EZI2C_1_sda__0__SHIFT 1u
#define EZI2C_1_sda__DR CYREG_PRT3_DR
#define EZI2C_1_sda__INTCFG CYREG_PRT3_INTCFG
#define EZI2C_1_sda__INTSTAT CYREG_PRT3_INTSTAT
#define EZI2C_1_sda__MASK 0x02u
#define EZI2C_1_sda__PA__CFG0 CYREG_UDB_PA3_CFG0
#define EZI2C_1_sda__PA__CFG1 CYREG_UDB_PA3_CFG1
#define EZI2C_1_sda__PA__CFG10 CYREG_UDB_PA3_CFG10
#define EZI2C_1_sda__PA__CFG11 CYREG_UDB_PA3_CFG11
#define EZI2C_1_sda__PA__CFG12 CYREG_UDB_PA3_CFG12
#define EZI2C_1_sda__PA__CFG13 CYREG_UDB_PA3_CFG13
#define EZI2C_1_sda__PA__CFG14 CYREG_UDB_PA3_CFG14
#define EZI2C_1_sda__PA__CFG2 CYREG_UDB_PA3_CFG2
#define EZI2C_1_sda__PA__CFG3 CYREG_UDB_PA3_CFG3
#define EZI2C_1_sda__PA__CFG4 CYREG_UDB_PA3_CFG4
#define EZI2C_1_sda__PA__CFG5 CYREG_UDB_PA3_CFG5
#define EZI2C_1_sda__PA__CFG6 CYREG_UDB_PA3_CFG6
#define EZI2C_1_sda__PA__CFG7 CYREG_UDB_PA3_CFG7
#define EZI2C_1_sda__PA__CFG8 CYREG_UDB_PA3_CFG8
#define EZI2C_1_sda__PA__CFG9 CYREG_UDB_PA3_CFG9
#define EZI2C_1_sda__PC CYREG_PRT3_PC
#define EZI2C_1_sda__PC2 CYREG_PRT3_PC2
#define EZI2C_1_sda__PORT 3u
#define EZI2C_1_sda__PS CYREG_PRT3_PS
#define EZI2C_1_sda__SHIFT 1u

/* LED */
#define LED__0__DM__MASK 0x1C0000u
#define LED__0__DM__SHIFT 18u
#define LED__0__DR CYREG_PRT1_DR
#define LED__0__HSIOM CYREG_HSIOM_PORT_SEL1
#define LED__0__HSIOM_MASK 0x0F000000u
#define LED__0__HSIOM_SHIFT 24u
#define LED__0__INTCFG CYREG_PRT1_INTCFG
#define LED__0__INTSTAT CYREG_PRT1_INTSTAT
#define LED__0__MASK 0x40u
#define LED__0__PA__CFG0 CYREG_UDB_PA1_CFG0
#define LED__0__PA__CFG1 CYREG_UDB_PA1_CFG1
#define LED__0__PA__CFG10 CYREG_UDB_PA1_CFG10
#define LED__0__PA__CFG11 CYREG_UDB_PA1_CFG11
#define LED__0__PA__CFG12 CYREG_UDB_PA1_CFG12
#define LED__0__PA__CFG13 CYREG_UDB_PA1_CFG13
#define LED__0__PA__CFG14 CYREG_UDB_PA1_CFG14
#define LED__0__PA__CFG2 CYREG_UDB_PA1_CFG2
#define LED__0__PA__CFG3 CYREG_UDB_PA1_CFG3
#define LED__0__PA__CFG4 CYREG_UDB_PA1_CFG4
#define LED__0__PA__CFG5 CYREG_UDB_PA1_CFG5
#define LED__0__PA__CFG6 CYREG_UDB_PA1_CFG6
#define LED__0__PA__CFG7 CYREG_UDB_PA1_CFG7
#define LED__0__PA__CFG8 CYREG_UDB_PA1_CFG8
#define LED__0__PA__CFG9 CYREG_UDB_PA1_CFG9
#define LED__0__PC CYREG_PRT1_PC
#define LED__0__PC2 CYREG_PRT1_PC2
#define LED__0__PORT 1u
#define LED__0__PS CYREG_PRT1_PS
#define LED__0__SHIFT 6u
#define LED__DR CYREG_PRT1_DR
#define LED__INTCFG CYREG_PRT1_INTCFG
#define LED__INTSTAT CYREG_PRT1_INTSTAT
#define LED__MASK 0x40u
#define LED__PA__CFG0 CYREG_UDB_PA1_CFG0
#define LED__PA__CFG1 CYREG_UDB_PA1_CFG1
#define LED__PA__CFG10 CYREG_UDB_PA1_CFG10
#define LED__PA__CFG11 CYREG_UDB_PA1_CFG11
#define LED__PA__CFG12 CYREG_UDB_PA1_CFG12
#define LED__PA__CFG13 CYREG_UDB_PA1_CFG13
#define LED__PA__CFG14 CYREG_UDB_PA1_CFG14
#define LED__PA__CFG2 CYREG_UDB_PA1_CFG2
#define LED__PA__CFG3 CYREG_UDB_PA1_CFG3
#define LED__PA__CFG4 CYREG_UDB_PA1_CFG4
#define LED__PA__CFG5 CYREG_UDB_PA1_CFG5
#define LED__PA__CFG6 CYREG_UDB_PA1_CFG6
#define LED__PA__CFG7 CYREG_UDB_PA1_CFG7
#define LED__PA__CFG8 CYREG_UDB_PA1_CFG8
#define LED__PA__CFG9 CYREG_UDB_PA1_CFG9
#define LED__PC CYREG_PRT1_PC
#define LED__PC2 CYREG_PRT1_PC2
#define LED__PORT 1u
#define LED__PS CYREG_PRT1_PS
#define LED__SHIFT 6u

/* Miscellaneous */
#define CY_PROJECT_NAME "Proto Board Test 1"
#define CY_VERSION "PSoC Creator  4.1 Update 1"
#define CYDEV_BANDGAP_VOLTAGE 1.024
#define CYDEV_BCLK__HFCLK__HZ 24000000U
#define CYDEV_BCLK__HFCLK__KHZ 24000U
#define CYDEV_BCLK__HFCLK__MHZ 24U
#define CYDEV_BCLK__SYSCLK__HZ 24000000U
#define CYDEV_BCLK__SYSCLK__KHZ 24000U
#define CYDEV_BCLK__SYSCLK__MHZ 24U
#define CYDEV_CHIP_DIE_LEOPARD 1u
#define CYDEV_CHIP_DIE_PSOC4A 16u
#define CYDEV_CHIP_DIE_PSOC5LP 2u
#define CYDEV_CHIP_DIE_PSOC5TM 3u
#define CYDEV_CHIP_DIE_TMA4 4u
#define CYDEV_CHIP_DIE_UNKNOWN 0u
#define CYDEV_CHIP_FAMILY_FM0P 5u
#define CYDEV_CHIP_FAMILY_FM3 6u
#define CYDEV_CHIP_FAMILY_FM4 7u
#define CYDEV_CHIP_FAMILY_PSOC3 1u
#define CYDEV_CHIP_FAMILY_PSOC4 2u
#define CYDEV_CHIP_FAMILY_PSOC5 3u
#define CYDEV_CHIP_FAMILY_PSOC6 4u
#define CYDEV_CHIP_FAMILY_UNKNOWN 0u
#define CYDEV_CHIP_FAMILY_USED CYDEV_CHIP_FAMILY_PSOC4
#define CYDEV_CHIP_JTAG_ID 0x04DB1193u
#define CYDEV_CHIP_MEMBER_3A 1u
#define CYDEV_CHIP_MEMBER_4A 16u
#define CYDEV_CHIP_MEMBER_4D 12u
#define CYDEV_CHIP_MEMBER_4E 6u
#define CYDEV_CHIP_MEMBER_4F 17u
#define CYDEV_CHIP_MEMBER_4G 4u
#define CYDEV_CHIP_MEMBER_4H 15u
#define CYDEV_CHIP_MEMBER_4I 21u
#define CYDEV_CHIP_MEMBER_4J 13u
#define CYDEV_CHIP_MEMBER_4K 14u
#define CYDEV_CHIP_MEMBER_4L 20u
#define CYDEV_CHIP_MEMBER_4M 19u
#define CYDEV_CHIP_MEMBER_4N 9u
#define CYDEV_CHIP_MEMBER_4O 7u
#define CYDEV_CHIP_MEMBER_4P 18u
#define CYDEV_CHIP_MEMBER_4Q 11u
#define CYDEV_CHIP_MEMBER_4R 8u
#define CYDEV_CHIP_MEMBER_4S 10u
#define CYDEV_CHIP_MEMBER_4U 5u
#define CYDEV_CHIP_MEMBER_5A 3u
#define CYDEV_CHIP_MEMBER_5B 2u
#define CYDEV_CHIP_MEMBER_6A 22u
#define CYDEV_CHIP_MEMBER_FM3 26u
#define CYDEV_CHIP_MEMBER_FM4 27u
#define CYDEV_CHIP_MEMBER_PDL_FM0P_TYPE1 23u
#define CYDEV_CHIP_MEMBER_PDL_FM0P_TYPE2 24u
#define CYDEV_CHIP_MEMBER_PDL_FM0P_TYPE3 25u
#define CYDEV_CHIP_MEMBER_UNKNOWN 0u
#define CYDEV_CHIP_MEMBER_USED CYDEV_CHIP_MEMBER_4A
#define CYDEV_CHIP_DIE_EXPECT CYDEV_CHIP_MEMBER_USED
#define CYDEV_CHIP_DIE_ACTUAL CYDEV_CHIP_DIE_EXPECT
#define CYDEV_CHIP_REV_LEOPARD_ES1 0u
#define CYDEV_CHIP_REV_LEOPARD_ES2 1u
#define CYDEV_CHIP_REV_LEOPARD_ES3 3u
#define CYDEV_CHIP_REV_LEOPARD_PRODUCTION 3u
#define CYDEV_CHIP_REV_PSOC4A_ES0 17u
#define CYDEV_CHIP_REV_PSOC4A_PRODUCTION 17u
#define CYDEV_CHIP_REV_PSOC5LP_ES0 0u
#define CYDEV_CHIP_REV_PSOC5LP_PRODUCTION 0u
#define CYDEV_CHIP_REV_PSOC5TM_ES0 0u
#define CYDEV_CHIP_REV_PSOC5TM_ES1 1u
#define CYDEV_CHIP_REV_PSOC5TM_PRODUCTION 1u
#define CYDEV_CHIP_REV_TMA4_ES 17u
#define CYDEV_CHIP_REV_TMA4_ES2 33u
#define CYDEV_CHIP_REV_TMA4_PRODUCTION 17u
#define CYDEV_CHIP_REVISION_3A_ES1 0u
#define CYDEV_CHIP_REVISION_3A_ES2 1u
#define CYDEV_CHIP_REVISION_3A_ES3 3u
#define CYDEV_CHIP_REVISION_3A_PRODUCTION 3u
#define CYDEV_CHIP_REVISION_4A_ES0 17u
#define CYDEV_CHIP_REVISION_4A_PRODUCTION 17u
#define CYDEV_CHIP_REVISION_4D_PRODUCTION 0u
#define CYDEV_CHIP_REVISION_4E_PRODUCTION 0u
#define CYDEV_CHIP_REVISION_4F_PRODUCTION 0u
#define CYDEV_CHIP_REVISION_4F_PRODUCTION_256DMA 0u
#define CYDEV_CHIP_REVISION_4F_PRODUCTION_256K 0u
#define CYDEV_CHIP_REVISION_4G_ES 17u
#define CYDEV_CHIP_REVISION_4G_ES2 33u
#define CYDEV_CHIP_REVISION_4G_PRODUCTION 17u
#define CYDEV_CHIP_REVISION_4H_PRODUCTION 0u
#define CYDEV_CHIP_REVISION_4I_PRODUCTION 0u
#define CYDEV_CHIP_REVISION_4J_PRODUCTION 0u
#define CYDEV_CHIP_REVISION_4K_PRODUCTION 0u
#define CYDEV_CHIP_REVISION_4L_PRODUCTION 0u
#define CYDEV_CHIP_REVISION_4M_PRODUCTION 0u
#define CYDEV_CHIP_REVISION_4N_PRODUCTION 0u
#define CYDEV_CHIP_REVISION_4O_PRODUCTION 0u
#define CYDEV_CHIP_REVISION_4P_PRODUCTION 0u
#define CYDEV_CHIP_REVISION_4Q_PRODUCTION 0u
#define CYDEV_CHIP_REVISION_4R_PRODUCTION 0u
#define CYDEV_CHIP_REVISION_4S_PRODUCTION 0u
#define CYDEV_CHIP_REVISION_4U_PRODUCTION 0u
#define CYDEV_CHIP_REVISION_5A_ES0 0u
#define CYDEV_CHIP_REVISION_5A_ES1 1u
#define CYDEV_CHIP_REVISION_5A_PRODUCTION 1u
#define CYDEV_CHIP_REVISION_5B_ES0 0u
#define CYDEV_CHIP_REVISION_5B_PRODUCTION 0u
#define CYDEV_CHIP_REVISION_6A_NO_UDB 0u
#define CYDEV_CHIP_REVISION_6A_PRODUCTION 0u
#define CYDEV_CHIP_REVISION_FM3_PRODUCTION 0u
#define CYDEV_CHIP_REVISION_FM4_PRODUCTION 0u
#define CYDEV_CHIP_REVISION_PDL_FM0P_TYPE1_PRODUCTION 0u
#define CYDEV_CHIP_REVISION_PDL_FM0P_TYPE2_PRODUCTION 0u
#define CYDEV_CHIP_REVISION_PDL_FM0P_TYPE3_PRODUCTION 0u
#define CYDEV_CHIP_REVISION_USED CYDEV_CHIP_REVISION_4A_PRODUCTION
#define CYDEV_CHIP_REV_EXPECT CYDEV_CHIP_REVISION_USED
#define CYDEV_CONFIG_READ_ACCELERATOR 1
#define CYDEV_CONFIG_UNUSED_IO_AllowButWarn 0
#define CYDEV_CONFIG_UNUSED_IO_AllowWithInfo 1
#define CYDEV_CONFIG_UNUSED_IO_Disallowed 2
#define CYDEV_CONFIG_UNUSED_IO CYDEV_CONFIG_UNUSED_IO_Disallowed
#define CYDEV_CONFIGURATION_COMPRESSED 1
#define CYDEV_CONFIGURATION_MODE_COMPRESSED 0
#define CYDEV_CONFIGURATION_MODE CYDEV_CONFIGURATION_MODE_COMPRESSED
#define CYDEV_CONFIGURATION_MODE_DMA 2
#define CYDEV_CONFIGURATION_MODE_UNCOMPRESSED 1
#define CYDEV_DEBUG_PROTECT_KILL 4
#define CYDEV_DEBUG_PROTECT_OPEN 1
#define CYDEV_DEBUG_PROTECT CYDEV_DEBUG_PROTECT_OPEN
#define CYDEV_DEBUG_PROTECT_PROTECTED 2
#define CYDEV_DEBUGGING_DPS_Disable 3
#define CYDEV_DEBUGGING_DPS_SWD 2
#define CYDEV_DEBUGGING_DPS CYDEV_DEBUGGING_DPS_SWD
#define CYDEV_DEBUGGING_ENABLE 1
#define CYDEV_DFT_SELECT_CLK0 1u
#define CYDEV_DFT_SELECT_CLK1 2u
#define CYDEV_HEAP_SIZE 0x80
#define CYDEV_IMO_TRIMMED_BY_USB 0u
#define CYDEV_IMO_TRIMMED_BY_WCO 0u
#define CYDEV_IS_EXPORTING_CODE 0
#define CYDEV_IS_IMPORTING_CODE 0
#define CYDEV_PROJ_TYPE 0
#define CYDEV_PROJ_TYPE_BOOTLOADER 1
#define CYDEV_PROJ_TYPE_LAUNCHER 5
#define CYDEV_PROJ_TYPE_LOADABLE 2
#define CYDEV_PROJ_TYPE_LOADABLEANDBOOTLOADER 4
#define CYDEV_PROJ_TYPE_MULTIAPPBOOTLOADER 3
#define CYDEV_PROJ_TYPE_STANDARD 0
#define CYDEV_STACK_SIZE 0x0400
#define CYDEV_USE_BUNDLED_CMSIS 1
#define CYDEV_VARIABLE_VDDA 1
#define CYDEV_VDDA 3.3
#define CYDEV_VDDA_MV 3300
#define CYDEV_VDDD 3.3
#define CYDEV_VDDD_MV 3300
#define CYDEV_WDT_GENERATE_ISR 1u
#define CYIPBLOCK_M0S8_CTBM_VERSION 0
#define CYIPBLOCK_m0s8cpuss_VERSION 0
#define CYIPBLOCK_m0s8gpio2_VERSION 0
#define CYIPBLOCK_m0s8hsiom4a_VERSION 0
#define CYIPBLOCK_m0s8lpcomp_VERSION 0
#define CYIPBLOCK_m0s8pclk_VERSION 0
#define CYIPBLOCK_m0s8sar_VERSION 0
#define CYIPBLOCK_m0s8scb_VERSION 0
#define CYIPBLOCK_m0s8srssv2_VERSION 1
#define CYIPBLOCK_m0s8tcpwm_VERSION 0
#define CYIPBLOCK_m0s8udbif_VERSION 0
#define CYIPBLOCK_S8_GPIO_VERSION 2
#define CYDEV_BOOTLOADER_ENABLE 0

#endif /* INCLUDED_CYFITTER_H */
