// ======================================================================
// Design01.v generated from TopDesign.cysch
// 09/19/2017 at 17:14
// This file is auto generated. ANY EDITS YOU MAKE MAY BE LOST WHEN THIS FILE IS REGENERATED!!!
// ======================================================================

/* -- WARNING: The following section of defines are deprecated and will be removed in a future release -- */
`define CYDEV_CHIP_DIE_LEOPARD 1
`define CYDEV_CHIP_REV_LEOPARD_PRODUCTION 3
`define CYDEV_CHIP_REV_LEOPARD_ES3 3
`define CYDEV_CHIP_REV_LEOPARD_ES2 1
`define CYDEV_CHIP_REV_LEOPARD_ES1 0
`define CYDEV_CHIP_DIE_PSOC5LP 2
`define CYDEV_CHIP_REV_PSOC5LP_PRODUCTION 0
`define CYDEV_CHIP_REV_PSOC5LP_ES0 0
`define CYDEV_CHIP_DIE_PSOC5TM 3
`define CYDEV_CHIP_REV_PSOC5TM_PRODUCTION 1
`define CYDEV_CHIP_REV_PSOC5TM_ES1 1
`define CYDEV_CHIP_REV_PSOC5TM_ES0 0
`define CYDEV_CHIP_DIE_TMA4 4
`define CYDEV_CHIP_REV_TMA4_PRODUCTION 17
`define CYDEV_CHIP_REV_TMA4_ES 17
`define CYDEV_CHIP_REV_TMA4_ES2 33
`define CYDEV_CHIP_DIE_PSOC4A 5
`define CYDEV_CHIP_REV_PSOC4A_PRODUCTION 17
`define CYDEV_CHIP_REV_PSOC4A_ES0 17
`define CYDEV_CHIP_DIE_PSOC6ABLE2 6
`define CYDEV_CHIP_REV_PSOC6ABLE2_PRODUCTION 0
`define CYDEV_CHIP_REV_PSOC6ABLE2_NO_UDB 0
`define CYDEV_CHIP_DIE_VOLANS 7
`define CYDEV_CHIP_REV_VOLANS_PRODUCTION 0
`define CYDEV_CHIP_DIE_BERRYPECKER 8
`define CYDEV_CHIP_REV_BERRYPECKER_PRODUCTION 0
`define CYDEV_CHIP_DIE_CRANE 9
`define CYDEV_CHIP_REV_CRANE_PRODUCTION 0
`define CYDEV_CHIP_DIE_FM3 10
`define CYDEV_CHIP_REV_FM3_PRODUCTION 0
`define CYDEV_CHIP_DIE_FM4 11
`define CYDEV_CHIP_REV_FM4_PRODUCTION 0
`define CYDEV_CHIP_DIE_EXPECT 2
`define CYDEV_CHIP_REV_EXPECT 0
`define CYDEV_CHIP_DIE_ACTUAL 2
/* -- WARNING: The previous section of defines are deprecated and will be removed in a future release -- */
`define CYDEV_CHIP_FAMILY_PSOC3 1
`define CYDEV_CHIP_FAMILY_PSOC4 2
`define CYDEV_CHIP_FAMILY_PSOC5 3
`define CYDEV_CHIP_FAMILY_PSOC6 4
`define CYDEV_CHIP_FAMILY_FM0P 5
`define CYDEV_CHIP_FAMILY_FM3 6
`define CYDEV_CHIP_FAMILY_FM4 7
`define CYDEV_CHIP_FAMILY_UNKNOWN 0
`define CYDEV_CHIP_MEMBER_UNKNOWN 0
`define CYDEV_CHIP_MEMBER_3A 1
`define CYDEV_CHIP_REVISION_3A_PRODUCTION 3
`define CYDEV_CHIP_REVISION_3A_ES3 3
`define CYDEV_CHIP_REVISION_3A_ES2 1
`define CYDEV_CHIP_REVISION_3A_ES1 0
`define CYDEV_CHIP_MEMBER_5B 2
`define CYDEV_CHIP_REVISION_5B_PRODUCTION 0
`define CYDEV_CHIP_REVISION_5B_ES0 0
`define CYDEV_CHIP_MEMBER_5A 3
`define CYDEV_CHIP_REVISION_5A_PRODUCTION 1
`define CYDEV_CHIP_REVISION_5A_ES1 1
`define CYDEV_CHIP_REVISION_5A_ES0 0
`define CYDEV_CHIP_MEMBER_4G 4
`define CYDEV_CHIP_REVISION_4G_PRODUCTION 17
`define CYDEV_CHIP_REVISION_4G_ES 17
`define CYDEV_CHIP_REVISION_4G_ES2 33
`define CYDEV_CHIP_MEMBER_4U 5
`define CYDEV_CHIP_REVISION_4U_PRODUCTION 0
`define CYDEV_CHIP_MEMBER_4E 6
`define CYDEV_CHIP_REVISION_4E_PRODUCTION 0
`define CYDEV_CHIP_MEMBER_4O 7
`define CYDEV_CHIP_REVISION_4O_PRODUCTION 0
`define CYDEV_CHIP_MEMBER_4R 8
`define CYDEV_CHIP_REVISION_4R_PRODUCTION 0
`define CYDEV_CHIP_MEMBER_4N 9
`define CYDEV_CHIP_REVISION_4N_PRODUCTION 0
`define CYDEV_CHIP_MEMBER_4S 10
`define CYDEV_CHIP_REVISION_4S_PRODUCTION 0
`define CYDEV_CHIP_MEMBER_4Q 11
`define CYDEV_CHIP_REVISION_4Q_PRODUCTION 0
`define CYDEV_CHIP_MEMBER_4D 12
`define CYDEV_CHIP_REVISION_4D_PRODUCTION 0
`define CYDEV_CHIP_MEMBER_4J 13
`define CYDEV_CHIP_REVISION_4J_PRODUCTION 0
`define CYDEV_CHIP_MEMBER_4K 14
`define CYDEV_CHIP_REVISION_4K_PRODUCTION 0
`define CYDEV_CHIP_MEMBER_4H 15
`define CYDEV_CHIP_REVISION_4H_PRODUCTION 0
`define CYDEV_CHIP_MEMBER_4A 16
`define CYDEV_CHIP_REVISION_4A_PRODUCTION 17
`define CYDEV_CHIP_REVISION_4A_ES0 17
`define CYDEV_CHIP_MEMBER_4F 17
`define CYDEV_CHIP_REVISION_4F_PRODUCTION 0
`define CYDEV_CHIP_REVISION_4F_PRODUCTION_256K 0
`define CYDEV_CHIP_REVISION_4F_PRODUCTION_256DMA 0
`define CYDEV_CHIP_MEMBER_4P 18
`define CYDEV_CHIP_REVISION_4P_PRODUCTION 0
`define CYDEV_CHIP_MEMBER_4M 19
`define CYDEV_CHIP_REVISION_4M_PRODUCTION 0
`define CYDEV_CHIP_MEMBER_4L 20
`define CYDEV_CHIP_REVISION_4L_PRODUCTION 0
`define CYDEV_CHIP_MEMBER_4I 21
`define CYDEV_CHIP_REVISION_4I_PRODUCTION 0
`define CYDEV_CHIP_MEMBER_6A 22
`define CYDEV_CHIP_REVISION_6A_PRODUCTION 0
`define CYDEV_CHIP_REVISION_6A_NO_UDB 0
`define CYDEV_CHIP_MEMBER_PDL_FM0P_TYPE1 23
`define CYDEV_CHIP_REVISION_PDL_FM0P_TYPE1_PRODUCTION 0
`define CYDEV_CHIP_MEMBER_PDL_FM0P_TYPE2 24
`define CYDEV_CHIP_REVISION_PDL_FM0P_TYPE2_PRODUCTION 0
`define CYDEV_CHIP_MEMBER_PDL_FM0P_TYPE3 25
`define CYDEV_CHIP_REVISION_PDL_FM0P_TYPE3_PRODUCTION 0
`define CYDEV_CHIP_MEMBER_FM3 26
`define CYDEV_CHIP_REVISION_FM3_PRODUCTION 0
`define CYDEV_CHIP_MEMBER_FM4 27
`define CYDEV_CHIP_REVISION_FM4_PRODUCTION 0
`define CYDEV_CHIP_FAMILY_USED 3
`define CYDEV_CHIP_MEMBER_USED 2
`define CYDEV_CHIP_REVISION_USED 0
// Component: cy_virtualmux_v1_0
`ifdef CY_BLK_DIR
`undef CY_BLK_DIR
`endif

`ifdef WARP
`define CY_BLK_DIR "C:\Program Files (x86)\Cypress\PSoC Creator\4.1\PSoC Creator\psoc\content\CyPrimitives\cyprimitives.cylib\cy_virtualmux_v1_0"
`include "C:\Program Files (x86)\Cypress\PSoC Creator\4.1\PSoC Creator\psoc\content\CyPrimitives\cyprimitives.cylib\cy_virtualmux_v1_0\cy_virtualmux_v1_0.v"
`else
`define CY_BLK_DIR "C:\Program Files (x86)\Cypress\PSoC Creator\4.1\PSoC Creator\psoc\content\CyPrimitives\cyprimitives.cylib\cy_virtualmux_v1_0"
`include "C:\Program Files (x86)\Cypress\PSoC Creator\4.1\PSoC Creator\psoc\content\CyPrimitives\cyprimitives.cylib\cy_virtualmux_v1_0\cy_virtualmux_v1_0.v"
`endif

// Component: ZeroTerminal
`ifdef CY_BLK_DIR
`undef CY_BLK_DIR
`endif

`ifdef WARP
`define CY_BLK_DIR "C:\Program Files (x86)\Cypress\PSoC Creator\4.1\PSoC Creator\psoc\content\CyPrimitives\cyprimitives.cylib\ZeroTerminal"
`include "C:\Program Files (x86)\Cypress\PSoC Creator\4.1\PSoC Creator\psoc\content\CyPrimitives\cyprimitives.cylib\ZeroTerminal\ZeroTerminal.v"
`else
`define CY_BLK_DIR "C:\Program Files (x86)\Cypress\PSoC Creator\4.1\PSoC Creator\psoc\content\CyPrimitives\cyprimitives.cylib\ZeroTerminal"
`include "C:\Program Files (x86)\Cypress\PSoC Creator\4.1\PSoC Creator\psoc\content\CyPrimitives\cyprimitives.cylib\ZeroTerminal\ZeroTerminal.v"
`endif

// USBFS_v3_20(AudioDescriptors=<?xml version="1.0" encoding="utf-16"?>\r\n<Tree xmlns:CustomizerVersion="3_20">\r\n  <Tree_x0020_Descriptors>\r\n    <DescriptorNode Key="Audio">\r\n      <Nodes />\r\n    </DescriptorNode>\r\n  </Tree_x0020_Descriptors>\r\n</Tree>, CDCDescriptors=<?xml version="1.0" encoding="utf-16"?>\r\n<Tree xmlns:CustomizerVersion="3_20">\r\n  <Tree_x0020_Descriptors>\r\n    <DescriptorNode Key="CDC">\r\n      <Nodes>\r\n        <DescriptorNode Key="Interface60">\r\n          <m_value d6p1:type="InterfaceGeneralDescriptor" xmlns:d6p1="http://www.w3.org/2001/XMLSchema-instance">\r\n            <bDescriptorType>ALTERNATE</bDescriptorType>\r\n            <bLength>0</bLength>\r\n            <DisplayName>CDC Interface 1</DisplayName>\r\n          </m_value>\r\n          <Value d6p1:type="InterfaceGeneralDescriptor" xmlns:d6p1="http://www.w3.org/2001/XMLSchema-instance">\r\n            <bDescriptorType>ALTERNATE</bDescriptorType>\r\n            <bLength>0</bLength>\r\n            <DisplayName>CDC Interface 1</DisplayName>\r\n          </Value>\r\n          <Nodes>\r\n            <DescriptorNode Key="USBDescriptor61">\r\n              <m_value d8p1:type="CyCommunicationsInterfaceDescriptor" xmlns:d8p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                <bDescriptorType>INTERFACE</bDescriptorType>\r\n                <bLength>9</bLength>\r\n                <iwInterface>49</iwInterface>\r\n                <bInterfaceClass>2</bInterfaceClass>\r\n                <bAlternateSetting>0</bAlternateSetting>\r\n                <bInterfaceNumber>0</bInterfaceNumber>\r\n                <bNumEndpoints>1</bNumEndpoints>\r\n                <bInterfaceSubClass>2</bInterfaceSubClass>\r\n                <bInterfaceProtocol>1</bInterfaceProtocol>\r\n                <iInterface>3</iInterface>\r\n                <sInterface>CDC Communication Interface</sInterface>\r\n              </m_value>\r\n              <Value d8p1:type="CyCommunicationsInterfaceDescriptor" xmlns:d8p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                <bDescriptorType>INTERFACE</bDescriptorType>\r\n                <bLength>9</bLength>\r\n                <iwInterface>49</iwInterface>\r\n                <bInterfaceClass>2</bInterfaceClass>\r\n                <bAlternateSetting>0</bAlternateSetting>\r\n                <bInterfaceNumber>0</bInterfaceNumber>\r\n                <bNumEndpoints>1</bNumEndpoints>\r\n                <bInterfaceSubClass>2</bInterfaceSubClass>\r\n                <bInterfaceProtocol>1</bInterfaceProtocol>\r\n                <iInterface>3</iInterface>\r\n                <sInterface>CDC Communication Interface</sInterface>\r\n              </Value>\r\n              <Nodes>\r\n                <DescriptorNode Key="USBDescriptor63">\r\n                  <m_value d10p1:type="CyCDCHeaderDescriptor" xmlns:d10p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                    <bDescriptorType>CDC</bDescriptorType>\r\n                    <bLength>5</bLength>\r\n                    <bDescriptorSubtype>HEADER</bDescriptorSubtype>\r\n                    <bcdADC>272</bcdADC>\r\n                  </m_value>\r\n                  <Value d10p1:type="CyCDCHeaderDescriptor" xmlns:d10p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                    <bDescriptorType>CDC</bDescriptorType>\r\n                    <bLength>5</bLength>\r\n                    <bDescriptorSubtype>HEADER</bDescriptorSubtype>\r\n                    <bcdADC>272</bcdADC>\r\n                  </Value>\r\n                  <Nodes />\r\n                </DescriptorNode>\r\n                <DescriptorNode Key="USBDescriptor64">\r\n                  <m_value d10p1:type="CyCDCAbstractControlMgmtDescriptor" xmlns:d10p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                    <bDescriptorType>CDC</bDescriptorType>\r\n                    <bLength>4</bLength>\r\n                    <bDescriptorSubtype>ABSTRACT_CONTROL_MANAGEMENT</bDescriptorSubtype>\r\n                    <bmCapabilities>2</bmCapabilities>\r\n                  </m_value>\r\n                  <Value d10p1:type="CyCDCAbstractControlMgmtDescriptor" xmlns:d10p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                    <bDescriptorType>CDC</bDescriptorType>\r\n                    <bLength>4</bLength>\r\n                    <bDescriptorSubtype>ABSTRACT_CONTROL_MANAGEMENT</bDescriptorSubtype>\r\n                    <bmCapabilities>2</bmCapabilities>\r\n                  </Value>\r\n                  <Nodes />\r\n                </DescriptorNode>\r\n                <DescriptorNode Key="USBDescriptor65">\r\n                  <m_value d10p1:type="CyCDCUnionDescriptor" xmlns:d10p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                    <bDescriptorType>CDC</bDescriptorType>\r\n                    <bLength>5</bLength>\r\n                    <bDescriptorSubtype>UNION</bDescriptorSubtype>\r\n                    <bSubordinateInterface>AQ==</bSubordinateInterface>\r\n                  </m_value>\r\n                  <Value d10p1:type="CyCDCUnionDescriptor" xmlns:d10p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                    <bDescriptorType>CDC</bDescriptorType>\r\n                    <bLength>5</bLength>\r\n                    <bDescriptorSubtype>UNION</bDescriptorSubtype>\r\n                    <bSubordinateInterface>AQ==</bSubordinateInterface>\r\n                  </Value>\r\n                  <Nodes />\r\n                </DescriptorNode>\r\n                <DescriptorNode Key="USBDescriptor66">\r\n                  <m_value d10p1:type="CyCDCCallManagementDescriptor" xmlns:d10p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                    <bDescriptorType>CDC</bDescriptorType>\r\n                    <bLength>5</bLength>\r\n                    <bDescriptorSubtype>CALL_MANAGEMENT</bDescriptorSubtype>\r\n                    <bDataInterface>1</bDataInterface>\r\n                  </m_value>\r\n                  <Value d10p1:type="CyCDCCallManagementDescriptor" xmlns:d10p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                    <bDescriptorType>CDC</bDescriptorType>\r\n                    <bLength>5</bLength>\r\n                    <bDescriptorSubtype>CALL_MANAGEMENT</bDescriptorSubtype>\r\n                    <bDataInterface>1</bDataInterface>\r\n                  </Value>\r\n                  <Nodes />\r\n                </DescriptorNode>\r\n                <DescriptorNode Key="USBDescriptor67">\r\n                  <m_value d10p1:type="EndpointDescriptor" xmlns:d10p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                    <bDescriptorType>ENDPOINT</bDescriptorType>\r\n                    <bLength>7</bLength>\r\n                    <DoubleBuffer>false</DoubleBuffer>\r\n                    <bEndpointAddress>129</bEndpointAddress>\r\n                    <bmAttributes>3</bmAttributes>\r\n                  </m_value>\r\n                  <Value d10p1:type="EndpointDescriptor" xmlns:d10p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                    <bDescriptorType>ENDPOINT</bDescriptorType>\r\n                    <bLength>7</bLength>\r\n                    <DoubleBuffer>false</DoubleBuffer>\r\n                    <bEndpointAddress>129</bEndpointAddress>\r\n                    <bmAttributes>3</bmAttributes>\r\n                  </Value>\r\n                  <Nodes />\r\n                </DescriptorNode>\r\n              </Nodes>\r\n            </DescriptorNode>\r\n          </Nodes>\r\n        </DescriptorNode>\r\n        <DescriptorNode Key="Interface68">\r\n          <m_value d6p1:type="InterfaceGeneralDescriptor" xmlns:d6p1="http://www.w3.org/2001/XMLSchema-instance">\r\n            <bDescriptorType>ALTERNATE</bDescriptorType>\r\n            <bLength>0</bLength>\r\n            <DisplayName>CDC Interface 2</DisplayName>\r\n          </m_value>\r\n          <Value d6p1:type="InterfaceGeneralDescriptor" xmlns:d6p1="http://www.w3.org/2001/XMLSchema-instance">\r\n            <bDescriptorType>ALTERNATE</bDescriptorType>\r\n            <bLength>0</bLength>\r\n            <DisplayName>CDC Interface 2</DisplayName>\r\n          </Value>\r\n          <Nodes>\r\n            <DescriptorNode Key="USBDescriptor69">\r\n              <m_value d8p1:type="CyDataInterfaceDescriptor" xmlns:d8p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                <bDescriptorType>INTERFACE</bDescriptorType>\r\n                <bLength>9</bLength>\r\n                <iwInterface>50</iwInterface>\r\n                <bInterfaceClass>10</bInterfaceClass>\r\n                <bAlternateSetting>0</bAlternateSetting>\r\n                <bInterfaceNumber>1</bInterfaceNumber>\r\n                <bNumEndpoints>2</bNumEndpoints>\r\n                <bInterfaceSubClass>0</bInterfaceSubClass>\r\n                <bInterfaceProtocol>0</bInterfaceProtocol>\r\n                <iInterface>4</iInterface>\r\n                <sInterface>CDC Data Interface</sInterface>\r\n              </m_value>\r\n              <Value d8p1:type="CyDataInterfaceDescriptor" xmlns:d8p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                <bDescriptorType>INTERFACE</bDescriptorType>\r\n                <bLength>9</bLength>\r\n                <iwInterface>50</iwInterface>\r\n                <bInterfaceClass>10</bInterfaceClass>\r\n                <bAlternateSetting>0</bAlternateSetting>\r\n                <bInterfaceNumber>1</bInterfaceNumber>\r\n                <bNumEndpoints>2</bNumEndpoints>\r\n                <bInterfaceSubClass>0</bInterfaceSubClass>\r\n                <bInterfaceProtocol>0</bInterfaceProtocol>\r\n                <iInterface>4</iInterface>\r\n                <sInterface>CDC Data Interface</sInterface>\r\n              </Value>\r\n              <Nodes>\r\n                <DescriptorNode Key="USBDescriptor71">\r\n                  <m_value d10p1:type="EndpointDescriptor" xmlns:d10p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                    <bDescriptorType>ENDPOINT</bDescriptorType>\r\n                    <bLength>7</bLength>\r\n                    <DoubleBuffer>false</DoubleBuffer>\r\n                    <bEndpointAddress>130</bEndpointAddress>\r\n                    <bmAttributes>2</bmAttributes>\r\n                    <wMaxPacketSize>64</wMaxPacketSize>\r\n                  </m_value>\r\n                  <Value d10p1:type="EndpointDescriptor" xmlns:d10p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                    <bDescriptorType>ENDPOINT</bDescriptorType>\r\n                    <bLength>7</bLength>\r\n                    <DoubleBuffer>false</DoubleBuffer>\r\n                    <bEndpointAddress>130</bEndpointAddress>\r\n                    <bmAttributes>2</bmAttributes>\r\n                    <wMaxPacketSize>64</wMaxPacketSize>\r\n                  </Value>\r\n                  <Nodes />\r\n                </DescriptorNode>\r\n                <DescriptorNode Key="USBDescriptor72">\r\n                  <m_value d10p1:type="EndpointDescriptor" xmlns:d10p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                    <bDescriptorType>ENDPOINT</bDescriptorType>\r\n                    <bLength>7</bLength>\r\n                    <DoubleBuffer>false</DoubleBuffer>\r\n                    <bEndpointAddress>3</bEndpointAddress>\r\n                    <bmAttributes>2</bmAttributes>\r\n                    <wMaxPacketSize>64</wMaxPacketSize>\r\n                  </m_value>\r\n                  <Value d10p1:type="EndpointDescriptor" xmlns:d10p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                    <bDescriptorType>ENDPOINT</bDescriptorType>\r\n                    <bLength>7</bLength>\r\n                    <DoubleBuffer>false</DoubleBuffer>\r\n                    <bEndpointAddress>3</bEndpointAddress>\r\n                    <bmAttributes>2</bmAttributes>\r\n                    <wMaxPacketSize>64</wMaxPacketSize>\r\n                  </Value>\r\n                  <Nodes />\r\n                </DescriptorNode>\r\n              </Nodes>\r\n            </DescriptorNode>\r\n          </Nodes>\r\n        </DescriptorNode>\r\n      </Nodes>\r\n    </DescriptorNode>\r\n  </Tree_x0020_Descriptors>\r\n</Tree>, DeviceDescriptors=<?xml version="1.0" encoding="utf-16"?>\r\n<Tree xmlns:CustomizerVersion="3_20">\r\n  <Tree_x0020_Descriptors>\r\n    <DescriptorNode Key="Device">\r\n      <Nodes>\r\n        <DescriptorNode Key="USBDescriptor51">\r\n          <m_value d6p1:type="DeviceDescriptor" xmlns:d6p1="http://www.w3.org/2001/XMLSchema-instance">\r\n            <bDescriptorType>DEVICE</bDescriptorType>\r\n            <bLength>18</bLength>\r\n            <iwManufacturer>47</iwManufacturer>\r\n            <iwProduct>48</iwProduct>\r\n            <sManufacturer>Cypress Semiconductor</sManufacturer>\r\n            <sProduct>USBUART</sProduct>\r\n            <sSerialNumber />\r\n            <bDeviceClass>2</bDeviceClass>\r\n            <bDeviceSubClass>0</bDeviceSubClass>\r\n            <bDeviceProtocol>0</bDeviceProtocol>\r\n            <bMaxPacketSize0>0</bMaxPacketSize0>\r\n            <idVendor>1204</idVendor>\r\n            <idProduct>8</idProduct>\r\n            <bcdDevice>1</bcdDevice>\r\n            <bcdUSB>512</bcdUSB>\r\n            <iManufacturer>1</iManufacturer>\r\n            <iProduct>2</iProduct>\r\n            <iSerialNumber>0</iSerialNumber>\r\n            <bNumConfigurations>1</bNumConfigurations>\r\n            <bMemoryMgmt>0</bMemoryMgmt>\r\n            <bMemoryAlloc>0</bMemoryAlloc>\r\n          </m_value>\r\n          <Value d6p1:type="DeviceDescriptor" xmlns:d6p1="http://www.w3.org/2001/XMLSchema-instance">\r\n            <bDescriptorType>DEVICE</bDescriptorType>\r\n            <bLength>18</bLength>\r\n            <iwManufacturer>47</iwManufacturer>\r\n            <iwProduct>48</iwProduct>\r\n            <sManufacturer>Cypress Semiconductor</sManufacturer>\r\n            <sProduct>USBUART</sProduct>\r\n            <sSerialNumber />\r\n            <bDeviceClass>2</bDeviceClass>\r\n            <bDeviceSubClass>0</bDeviceSubClass>\r\n            <bDeviceProtocol>0</bDeviceProtocol>\r\n            <bMaxPacketSize0>0</bMaxPacketSize0>\r\n            <idVendor>1204</idVendor>\r\n            <idProduct>8</idProduct>\r\n            <bcdDevice>1</bcdDevice>\r\n            <bcdUSB>512</bcdUSB>\r\n            <iManufacturer>1</iManufacturer>\r\n            <iProduct>2</iProduct>\r\n            <iSerialNumber>0</iSerialNumber>\r\n            <bNumConfigurations>1</bNumConfigurations>\r\n            <bMemoryMgmt>0</bMemoryMgmt>\r\n            <bMemoryAlloc>0</bMemoryAlloc>\r\n          </Value>\r\n          <Nodes>\r\n            <DescriptorNode Key="USBDescriptor56">\r\n              <m_value d8p1:type="ConfigDescriptor" xmlns:d8p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                <bDescriptorType>CONFIGURATION</bDescriptorType>\r\n                <bLength>9</bLength>\r\n                <iwConfiguration>47</iwConfiguration>\r\n                <sConfiguration>Cypress Semiconductor</sConfiguration>\r\n                <wTotalLength>67</wTotalLength>\r\n                <bNumInterfaces>2</bNumInterfaces>\r\n                <bConfigurationValue>0</bConfigurationValue>\r\n                <iConfiguration>1</iConfiguration>\r\n                <bmAttributes>128</bmAttributes>\r\n                <bMaxPower>50</bMaxPower>\r\n              </m_value>\r\n              <Value d8p1:type="ConfigDescriptor" xmlns:d8p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                <bDescriptorType>CONFIGURATION</bDescriptorType>\r\n                <bLength>9</bLength>\r\n                <iwConfiguration>47</iwConfiguration>\r\n                <sConfiguration>Cypress Semiconductor</sConfiguration>\r\n                <wTotalLength>67</wTotalLength>\r\n                <bNumInterfaces>2</bNumInterfaces>\r\n                <bConfigurationValue>0</bConfigurationValue>\r\n                <iConfiguration>1</iConfiguration>\r\n                <bmAttributes>128</bmAttributes>\r\n                <bMaxPower>50</bMaxPower>\r\n              </Value>\r\n              <Nodes>\r\n                <DescriptorNode Key="Interface60">\r\n                  <m_value d10p1:type="InterfaceGeneralDescriptor" xmlns:d10p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                    <bDescriptorType>ALTERNATE</bDescriptorType>\r\n                    <bLength>0</bLength>\r\n                    <DisplayName>CDC Interface 1</DisplayName>\r\n                  </m_value>\r\n                  <Value d10p1:type="InterfaceGeneralDescriptor" xmlns:d10p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                    <bDescriptorType>ALTERNATE</bDescriptorType>\r\n                    <bLength>0</bLength>\r\n                    <DisplayName>CDC Interface 1</DisplayName>\r\n                  </Value>\r\n                  <Nodes>\r\n                    <DescriptorNode Key="USBDescriptor61">\r\n                      <m_value d12p1:type="CyCommunicationsInterfaceDescriptor" xmlns:d12p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                        <bDescriptorType>INTERFACE</bDescriptorType>\r\n                        <bLength>9</bLength>\r\n                        <iwInterface>49</iwInterface>\r\n                        <bInterfaceClass>2</bInterfaceClass>\r\n                        <bAlternateSetting>0</bAlternateSetting>\r\n                        <bInterfaceNumber>0</bInterfaceNumber>\r\n                        <bNumEndpoints>1</bNumEndpoints>\r\n                        <bInterfaceSubClass>2</bInterfaceSubClass>\r\n                        <bInterfaceProtocol>1</bInterfaceProtocol>\r\n                        <iInterface>3</iInterface>\r\n                        <sInterface>CDC Communication Interface</sInterface>\r\n                      </m_value>\r\n                      <Value d12p1:type="CyCommunicationsInterfaceDescriptor" xmlns:d12p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                        <bDescriptorType>INTERFACE</bDescriptorType>\r\n                        <bLength>9</bLength>\r\n                        <iwInterface>49</iwInterface>\r\n                        <bInterfaceClass>2</bInterfaceClass>\r\n                        <bAlternateSetting>0</bAlternateSetting>\r\n                        <bInterfaceNumber>0</bInterfaceNumber>\r\n                        <bNumEndpoints>1</bNumEndpoints>\r\n                        <bInterfaceSubClass>2</bInterfaceSubClass>\r\n                        <bInterfaceProtocol>1</bInterfaceProtocol>\r\n                        <iInterface>3</iInterface>\r\n                        <sInterface>CDC Communication Interface</sInterface>\r\n                      </Value>\r\n                      <Nodes>\r\n                        <DescriptorNode Key="USBDescriptor63">\r\n                          <m_value d14p1:type="CyCDCHeaderDescriptor" xmlns:d14p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                            <bDescriptorType>CDC</bDescriptorType>\r\n                            <bLength>5</bLength>\r\n                            <bDescriptorSubtype>HEADER</bDescriptorSubtype>\r\n                            <bcdADC>272</bcdADC>\r\n                          </m_value>\r\n                          <Value d14p1:type="CyCDCHeaderDescriptor" xmlns:d14p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                            <bDescriptorType>CDC</bDescriptorType>\r\n                            <bLength>5</bLength>\r\n                            <bDescriptorSubtype>HEADER</bDescriptorSubtype>\r\n                            <bcdADC>272</bcdADC>\r\n                          </Value>\r\n                          <Nodes />\r\n                        </DescriptorNode>\r\n                        <DescriptorNode Key="USBDescriptor64">\r\n                          <m_value d14p1:type="CyCDCAbstractControlMgmtDescriptor" xmlns:d14p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                            <bDescriptorType>CDC</bDescriptorType>\r\n                            <bLength>4</bLength>\r\n                            <bDescriptorSubtype>ABSTRACT_CONTROL_MANAGEMENT</bDescriptorSubtype>\r\n                            <bmCapabilities>2</bmCapabilities>\r\n                          </m_value>\r\n                          <Value d14p1:type="CyCDCAbstractControlMgmtDescriptor" xmlns:d14p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                            <bDescriptorType>CDC</bDescriptorType>\r\n                            <bLength>4</bLength>\r\n                            <bDescriptorSubtype>ABSTRACT_CONTROL_MANAGEMENT</bDescriptorSubtype>\r\n                            <bmCapabilities>2</bmCapabilities>\r\n                          </Value>\r\n                          <Nodes />\r\n                        </DescriptorNode>\r\n                        <DescriptorNode Key="USBDescriptor65">\r\n                          <m_value d14p1:type="CyCDCUnionDescriptor" xmlns:d14p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                            <bDescriptorType>CDC</bDescriptorType>\r\n                            <bLength>5</bLength>\r\n                            <bDescriptorSubtype>UNION</bDescriptorSubtype>\r\n                            <bSubordinateInterface>AQ==</bSubordinateInterface>\r\n                          </m_value>\r\n                          <Value d14p1:type="CyCDCUnionDescriptor" xmlns:d14p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                            <bDescriptorType>CDC</bDescriptorType>\r\n                            <bLength>5</bLength>\r\n                            <bDescriptorSubtype>UNION</bDescriptorSubtype>\r\n                            <bSubordinateInterface>AQ==</bSubordinateInterface>\r\n                          </Value>\r\n                          <Nodes />\r\n                        </DescriptorNode>\r\n                        <DescriptorNode Key="USBDescriptor66">\r\n                          <m_value d14p1:type="CyCDCCallManagementDescriptor" xmlns:d14p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                            <bDescriptorType>CDC</bDescriptorType>\r\n                            <bLength>5</bLength>\r\n                            <bDescriptorSubtype>CALL_MANAGEMENT</bDescriptorSubtype>\r\n                            <bDataInterface>1</bDataInterface>\r\n                          </m_value>\r\n                          <Value d14p1:type="CyCDCCallManagementDescriptor" xmlns:d14p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                            <bDescriptorType>CDC</bDescriptorType>\r\n                            <bLength>5</bLength>\r\n                            <bDescriptorSubtype>CALL_MANAGEMENT</bDescriptorSubtype>\r\n                            <bDataInterface>1</bDataInterface>\r\n                          </Value>\r\n                          <Nodes />\r\n                        </DescriptorNode>\r\n                        <DescriptorNode Key="USBDescriptor67">\r\n                          <m_value d14p1:type="EndpointDescriptor" xmlns:d14p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                            <bDescriptorType>ENDPOINT</bDescriptorType>\r\n                            <bLength>7</bLength>\r\n                            <DoubleBuffer>false</DoubleBuffer>\r\n                            <bEndpointAddress>129</bEndpointAddress>\r\n                            <bmAttributes>3</bmAttributes>\r\n                          </m_value>\r\n                          <Value d14p1:type="EndpointDescriptor" xmlns:d14p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                            <bDescriptorType>ENDPOINT</bDescriptorType>\r\n                            <bLength>7</bLength>\r\n                            <DoubleBuffer>false</DoubleBuffer>\r\n                            <bEndpointAddress>129</bEndpointAddress>\r\n                            <bmAttributes>3</bmAttributes>\r\n                          </Value>\r\n                          <Nodes />\r\n                        </DescriptorNode>\r\n                      </Nodes>\r\n                    </DescriptorNode>\r\n                  </Nodes>\r\n                </DescriptorNode>\r\n                <DescriptorNode Key="Interface68">\r\n                  <m_value d10p1:type="InterfaceGeneralDescriptor" xmlns:d10p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                    <bDescriptorType>ALTERNATE</bDescriptorType>\r\n                    <bLength>0</bLength>\r\n                    <DisplayName>CDC Interface 2</DisplayName>\r\n                  </m_value>\r\n                  <Value d10p1:type="InterfaceGeneralDescriptor" xmlns:d10p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                    <bDescriptorType>ALTERNATE</bDescriptorType>\r\n                    <bLength>0</bLength>\r\n                    <DisplayName>CDC Interface 2</DisplayName>\r\n                  </Value>\r\n                  <Nodes>\r\n                    <DescriptorNode Key="USBDescriptor69">\r\n                      <m_value d12p1:type="CyDataInterfaceDescriptor" xmlns:d12p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                        <bDescriptorType>INTERFACE</bDescriptorType>\r\n                        <bLength>9</bLength>\r\n                        <iwInterface>50</iwInterface>\r\n                        <bInterfaceClass>10</bInterfaceClass>\r\n                        <bAlternateSetting>0</bAlternateSetting>\r\n                        <bInterfaceNumber>1</bInterfaceNumber>\r\n                        <bNumEndpoints>2</bNumEndpoints>\r\n                        <bInterfaceSubClass>0</bInterfaceSubClass>\r\n                        <bInterfaceProtocol>0</bInterfaceProtocol>\r\n                        <iInterface>4</iInterface>\r\n                        <sInterface>CDC Data Interface</sInterface>\r\n                      </m_value>\r\n                      <Value d12p1:type="CyDataInterfaceDescriptor" xmlns:d12p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                        <bDescriptorType>INTERFACE</bDescriptorType>\r\n                        <bLength>9</bLength>\r\n                        <iwInterface>50</iwInterface>\r\n                        <bInterfaceClass>10</bInterfaceClass>\r\n                        <bAlternateSetting>0</bAlternateSetting>\r\n                        <bInterfaceNumber>1</bInterfaceNumber>\r\n                        <bNumEndpoints>2</bNumEndpoints>\r\n                        <bInterfaceSubClass>0</bInterfaceSubClass>\r\n                        <bInterfaceProtocol>0</bInterfaceProtocol>\r\n                        <iInterface>4</iInterface>\r\n                        <sInterface>CDC Data Interface</sInterface>\r\n                      </Value>\r\n                      <Nodes>\r\n                        <DescriptorNode Key="USBDescriptor71">\r\n                          <m_value d14p1:type="EndpointDescriptor" xmlns:d14p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                            <bDescriptorType>ENDPOINT</bDescriptorType>\r\n                            <bLength>7</bLength>\r\n                            <DoubleBuffer>false</DoubleBuffer>\r\n                            <bEndpointAddress>130</bEndpointAddress>\r\n                            <bmAttributes>2</bmAttributes>\r\n                            <wMaxPacketSize>64</wMaxPacketSize>\r\n                          </m_value>\r\n                          <Value d14p1:type="EndpointDescriptor" xmlns:d14p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                            <bDescriptorType>ENDPOINT</bDescriptorType>\r\n                            <bLength>7</bLength>\r\n                            <DoubleBuffer>false</DoubleBuffer>\r\n                            <bEndpointAddress>130</bEndpointAddress>\r\n                            <bmAttributes>2</bmAttributes>\r\n                            <wMaxPacketSize>64</wMaxPacketSize>\r\n                          </Value>\r\n                          <Nodes />\r\n                        </DescriptorNode>\r\n                        <DescriptorNode Key="USBDescriptor72">\r\n                          <m_value d14p1:type="EndpointDescriptor" xmlns:d14p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                            <bDescriptorType>ENDPOINT</bDescriptorType>\r\n                            <bLength>7</bLength>\r\n                            <DoubleBuffer>false</DoubleBuffer>\r\n                            <bEndpointAddress>3</bEndpointAddress>\r\n                            <bmAttributes>2</bmAttributes>\r\n                            <wMaxPacketSize>64</wMaxPacketSize>\r\n                          </m_value>\r\n                          <Value d14p1:type="EndpointDescriptor" xmlns:d14p1="http://www.w3.org/2001/XMLSchema-instance">\r\n                            <bDescriptorType>ENDPOINT</bDescriptorType>\r\n                            <bLength>7</bLength>\r\n                            <DoubleBuffer>false</DoubleBuffer>\r\n                            <bEndpointAddress>3</bEndpointAddress>\r\n                            <bmAttributes>2</bmAttributes>\r\n                            <wMaxPacketSize>64</wMaxPacketSize>\r\n                          </Value>\r\n                          <Nodes />\r\n                        </DescriptorNode>\r\n                      </Nodes>\r\n                    </DescriptorNode>\r\n                  </Nodes>\r\n                </DescriptorNode>\r\n              </Nodes>\r\n            </DescriptorNode>\r\n          </Nodes>\r\n        </DescriptorNode>\r\n      </Nodes>\r\n    </DescriptorNode>\r\n  </Tree_x0020_Descriptors>\r\n</Tree>, DmaChannelPriority=3, DW_Hide_DmaAuto=true, DW_Hide_Usbv2Regs=true, DW_RegSize=8, DW_USB_CHGDET_CTRL=CR0, DW_USB_INTR_CAUSE_HI=CR0, DW_USB_INTR_CAUSE_LO=CR0, DW_USB_INTR_CAUSE_MED=CR0, DW_USB_INTR_LVL_SEL=CR0, DW_USB_INTR_SIE=CR0, DW_USB_INTR_SIE_MASK=CR0, DW_USB_LPM_CTRL=CR0, DW_USB_LPM_STAT=CR0, DW_USB_POWER_CTRL=CR0, EnableBatteryChargDetect=false, EnableCDCApi=true, EnableMidiApi=true, endpointMA=0, endpointMM=0, epDMAautoOptimization=false, extern_cls=false, extern_vbus=false, extern_vnd=false, extJackCount=0, Gen16bitEpAccessApi=true, HandleMscRequests=true, HIDReportDescriptors=<?xml version="1.0" encoding="utf-16"?>\r\n<Tree xmlns:CustomizerVersion="3_20">\r\n  <Tree_x0020_Descriptors>\r\n    <DescriptorNode Key="HIDReport">\r\n      <Nodes />\r\n    </DescriptorNode>\r\n  </Tree_x0020_Descriptors>\r\n</Tree>, isrGroupArbiter=0, isrGroupBusReset=2, isrGroupEp0=1, isrGroupEp1=1, isrGroupEp2=1, isrGroupEp3=1, isrGroupEp4=1, isrGroupEp5=1, isrGroupEp6=1, isrGroupEp7=1, isrGroupEp8=1, isrGroupLpm=0, isrGroupSof=2, M0S8USBDSS_BLOCK_COUNT_1=0, max_interfaces_num=2, MidiDescriptors=<?xml version="1.0" encoding="utf-16"?>\r\n<Tree xmlns:CustomizerVersion="3_20">\r\n  <Tree_x0020_Descriptors>\r\n    <DescriptorNode Key="Midi">\r\n      <Nodes />\r\n    </DescriptorNode>\r\n  </Tree_x0020_Descriptors>\r\n</Tree>, Mode=false, mon_vbus=false, MscDescriptors=, MscLogicalUnitsNum=1, out_sof=false, Pid=0008, powerpad_vbus=false, PRIMITIVE_INSTANCE=USB, ProdactName=, ProdactRevision=, REG_SIZE=reg8, RemoveDmaAutoOpt=true, RemoveVbusPin=true, rm_arb_int=false, rm_dma_1=true, rm_dma_2=true, rm_dma_3=true, rm_dma_4=true, rm_dma_5=true, rm_dma_6=true, rm_dma_7=true, rm_dma_8=true, rm_dp_int=false, rm_ep_isr_0=false, rm_ep_isr_1=false, rm_ep_isr_2=false, rm_ep_isr_3=false, rm_ep_isr_4=true, rm_ep_isr_5=true, rm_ep_isr_6=true, rm_ep_isr_7=true, rm_ep_isr_8=true, rm_lpm_int=true, rm_ord_int=true, rm_sof_int=false, rm_usb_int=false, SofTermEnable=false, StringDescriptors=<?xml version="1.0" encoding="utf-16"?>\r\n<Tree xmlns:CustomizerVersion="3_20">\r\n  <Tree_x0020_Descriptors>\r\n    <DescriptorNode Key="String">\r\n      <Nodes>\r\n        <DescriptorNode Key="LANGID">\r\n          <m_value d6p1:type="StringZeroDescriptor" xmlns:d6p1="http://www.w3.org/2001/XMLSchema-instance">\r\n            <bDescriptorType>STRING</bDescriptorType>\r\n            <bLength>4</bLength>\r\n            <wLANGID>1033</wLANGID>\r\n          </m_value>\r\n          <Value d6p1:type="StringZeroDescriptor" xmlns:d6p1="http://www.w3.org/2001/XMLSchema-instance">\r\n            <bDescriptorType>STRING</bDescriptorType>\r\n            <bLength>4</bLength>\r\n            <wLANGID>1033</wLANGID>\r\n          </Value>\r\n          <Nodes />\r\n        </DescriptorNode>\r\n        <DescriptorNode Key="USBDescriptor47">\r\n          <m_value d6p1:type="StringDescriptor" xmlns:d6p1="http://www.w3.org/2001/XMLSchema-instance">\r\n            <bDescriptorType>STRING</bDescriptorType>\r\n            <bLength>44</bLength>\r\n            <snType>USER_ENTERED_TEXT</snType>\r\n            <bString>Cypress Semiconductor</bString>\r\n            <bUsed>false</bUsed>\r\n          </m_value>\r\n          <Value d6p1:type="StringDescriptor" xmlns:d6p1="http://www.w3.org/2001/XMLSchema-instance">\r\n            <bDescriptorType>STRING</bDescriptorType>\r\n            <bLength>44</bLength>\r\n            <snType>USER_ENTERED_TEXT</snType>\r\n            <bString>Cypress Semiconductor</bString>\r\n            <bUsed>false</bUsed>\r\n          </Value>\r\n          <Nodes />\r\n        </DescriptorNode>\r\n        <DescriptorNode Key="USBDescriptor48">\r\n          <m_value d6p1:type="StringDescriptor" xmlns:d6p1="http://www.w3.org/2001/XMLSchema-instance">\r\n            <bDescriptorType>STRING</bDescriptorType>\r\n            <bLength>16</bLength>\r\n            <snType>USER_ENTERED_TEXT</snType>\r\n            <bString>USBUART</bString>\r\n            <bUsed>false</bUsed>\r\n          </m_value>\r\n          <Value d6p1:type="StringDescriptor" xmlns:d6p1="http://www.w3.org/2001/XMLSchema-instance">\r\n            <bDescriptorType>STRING</bDescriptorType>\r\n            <bLength>16</bLength>\r\n            <snType>USER_ENTERED_TEXT</snType>\r\n            <bString>USBUART</bString>\r\n            <bUsed>false</bUsed>\r\n          </Value>\r\n          <Nodes />\r\n        </DescriptorNode>\r\n        <DescriptorNode Key="USBDescriptor49">\r\n          <m_value d6p1:type="StringDescriptor" xmlns:d6p1="http://www.w3.org/2001/XMLSchema-instance">\r\n            <bDescriptorType>STRING</bDescriptorType>\r\n            <bLength>56</bLength>\r\n            <snType>USER_ENTERED_TEXT</snType>\r\n            <bString>CDC Communication Interface</bString>\r\n            <bUsed>false</bUsed>\r\n          </m_value>\r\n          <Value d6p1:type="StringDescriptor" xmlns:d6p1="http://www.w3.org/2001/XMLSchema-instance">\r\n            <bDescriptorType>STRING</bDescriptorType>\r\n            <bLength>56</bLength>\r\n            <snType>USER_ENTERED_TEXT</snType>\r\n            <bString>CDC Communication Interface</bString>\r\n            <bUsed>false</bUsed>\r\n          </Value>\r\n          <Nodes />\r\n        </DescriptorNode>\r\n        <DescriptorNode Key="USBDescriptor50">\r\n          <m_value d6p1:type="StringDescriptor" xmlns:d6p1="http://www.w3.org/2001/XMLSchema-instance">\r\n            <bDescriptorType>STRING</bDescriptorType>\r\n            <bLength>38</bLength>\r\n            <snType>USER_ENTERED_TEXT</snType>\r\n            <bString>CDC Data Interface</bString>\r\n            <bUsed>false</bUsed>\r\n          </m_value>\r\n          <Value d6p1:type="StringDescriptor" xmlns:d6p1="http://www.w3.org/2001/XMLSchema-instance">\r\n            <bDescriptorType>STRING</bDescriptorType>\r\n            <bLength>38</bLength>\r\n            <snType>USER_ENTERED_TEXT</snType>\r\n            <bString>CDC Data Interface</bString>\r\n            <bUsed>false</bUsed>\r\n          </Value>\r\n          <Nodes />\r\n        </DescriptorNode>\r\n      </Nodes>\r\n    </DescriptorNode>\r\n    <DescriptorNode Key="SpecialString">\r\n      <Nodes>\r\n        <DescriptorNode Key="Serial">\r\n          <m_value d6p1:type="StringDescriptor" xmlns:d6p1="http://www.w3.org/2001/XMLSchema-instance">\r\n            <bDescriptorType>STRING</bDescriptorType>\r\n            <bLength>2</bLength>\r\n            <snType>SILICON_NUMBER</snType>\r\n            <bString />\r\n            <bUsed>true</bUsed>\r\n          </m_value>\r\n          <Value d6p1:type="StringDescriptor" xmlns:d6p1="http://www.w3.org/2001/XMLSchema-instance">\r\n            <bDescriptorType>STRING</bDescriptorType>\r\n            <bLength>2</bLength>\r\n            <snType>SILICON_NUMBER</snType>\r\n            <bString />\r\n            <bUsed>true</bUsed>\r\n          </Value>\r\n          <Nodes />\r\n        </DescriptorNode>\r\n        <DescriptorNode Key="EE">\r\n          <m_value d6p1:type="StringDescriptor" xmlns:d6p1="http://www.w3.org/2001/XMLSchema-instance">\r\n            <bDescriptorType>STRING</bDescriptorType>\r\n            <bLength>16</bLength>\r\n            <snType>USER_ENTERED_TEXT</snType>\r\n            <bString>MSFT100</bString>\r\n            <bUsed>false</bUsed>\r\n          </m_value>\r\n          <Value d6p1:type="StringDescriptor" xmlns:d6p1="http://www.w3.org/2001/XMLSchema-instance">\r\n            <bDescriptorType>STRING</bDescriptorType>\r\n            <bLength>16</bLength>\r\n            <snType>USER_ENTERED_TEXT</snType>\r\n            <bString>MSFT100</bString>\r\n            <bUsed>false</bUsed>\r\n          </Value>\r\n          <Nodes />\r\n        </DescriptorNode>\r\n      </Nodes>\r\n    </DescriptorNode>\r\n  </Tree_x0020_Descriptors>\r\n</Tree>, UINT_TYPE=uint8, VbusDetectTermEnable=false, VendorName=, Vid=04B4, CY_API_CALLBACK_HEADER_INCLUDE=#include "cyapicallbacks.h", CY_COMMENT=, CY_COMPONENT_NAME=USBFS_v3_20, CY_CONST_CONFIG=true, CY_CONTROL_FILE=<:default:>, CY_DATASHEET_FILE=<:default:>, CY_FITTER_NAME=USBUART, CY_INSTANCE_SHORT_NAME=USBUART, CY_MAJOR_VERSION=3, CY_MINOR_VERSION=20, CY_PDL_DRIVER_NAME=, CY_PDL_DRIVER_REQ_VERSION=, CY_PDL_DRIVER_SUBGROUP=, CY_PDL_DRIVER_VARIANT=, CY_REMOVE=false, CY_SUPPRESS_API_GEN=false, CY_VERSION=PSoC Creator  4.1 Update 1, INSTANCE_NAME=USBUART, )
module USBFS_v3_20_0 (
    sof,
    vbusdet);
    output      sof;
    input       vbusdet;

    parameter epDMAautoOptimization = 0;

          wire  Net_1914;
          wire  Net_1915;
          wire  Net_1916;
          wire  Net_1917;
          wire  Net_1918;
          wire  Net_1919;
          wire [7:0] dma_request;
          wire  Net_1920;
          wire  Net_1921;
          wire  Net_1922;
          wire [7:0] Net_2039;
          wire  Net_2038;
          wire  Net_2037;
          wire  EPs_1_to_7_dma_complete;
          wire  Net_2036;
          wire  Net_2035;
          wire  Net_2034;
          wire  Net_2033;
          wire  Net_2032;
          wire  Net_2031;
          wire  Net_2030;
          wire  Net_2029;
          wire  Net_2028;
          wire  Net_2027;
          wire  Net_2026;
          wire  Net_2025;
          wire  Net_2024;
          wire [7:0] Net_1940;
          wire  Net_1939;
          wire  Net_1938;
          wire  Net_1937;
          wire  Net_1936;
          wire  Net_1935;
          wire  Net_1934;
          wire  Net_1933;
          wire  Net_1932;
          wire  Net_2047;
          wire  Net_1202;
          wire  dma_terminate;
          wire [7:0] Net_2040;
          wire  Net_1010;
    electrical  Net_1000;
    electrical  Net_597;
          wire  Net_1495;
          wire  Net_1498;
          wire  Net_1559;
          wire  Net_1567;
          wire  Net_1576;
          wire  Net_1579;
          wire  Net_1591;
          wire [7:0] dma_complete;
          wire  Net_1588;
          wire  Net_1876;
          wire [8:0] ep_int;
          wire  Net_1889;
          wire  busClk;
          wire  Net_95;


	cy_isr_v1_0
		#(.int_type(2'b10))
		dp_int
		 (.int_signal(Net_1010));


	wire [0:0] tmpOE__Dm_net;
	wire [0:0] tmpFB_0__Dm_net;
	wire [0:0] tmpIO_0__Dm_net;
	wire [0:0] tmpINTERRUPT_0__Dm_net;
	electrical [0:0] tmpSIOVREF__Dm_net;

	cy_psoc3_pins_v1_10
		#(.id("beca5e2d-f70f-4900-a4db-7eca1ed3126e/8b77a6c4-10a0-4390-971c-672353e2a49c"),
		  .drive_mode(3'b000),
		  .ibuf_enabled(1'b0),
		  .init_dr_st(1'b0),
		  .input_clk_en(0),
		  .input_sync(1'b1),
		  .input_sync_mode(1'b0),
		  .intr_mode(2'b00),
		  .invert_in_clock(0),
		  .invert_in_clock_en(0),
		  .invert_in_reset(0),
		  .invert_out_clock(0),
		  .invert_out_clock_en(0),
		  .invert_out_reset(0),
		  .io_voltage(""),
		  .layout_mode("NONCONTIGUOUS"),
		  .oe_conn(1'b0),
		  .oe_reset(0),
		  .oe_sync(1'b0),
		  .output_clk_en(0),
		  .output_clock_mode(1'b0),
		  .output_conn(1'b0),
		  .output_mode(1'b0),
		  .output_reset(0),
		  .output_sync(1'b0),
		  .pa_in_clock(-1),
		  .pa_in_clock_en(-1),
		  .pa_in_reset(-1),
		  .pa_out_clock(-1),
		  .pa_out_clock_en(-1),
		  .pa_out_reset(-1),
		  .pin_aliases(""),
		  .pin_mode("A"),
		  .por_state(4),
		  .sio_group_cnt(0),
		  .sio_hyst(1'b1),
		  .sio_ibuf(""),
		  .sio_info(2'b00),
		  .sio_obuf(""),
		  .sio_refsel(""),
		  .sio_vtrip(""),
		  .sio_hifreq(""),
		  .sio_vohsel(""),
		  .slew_rate(1'b0),
		  .spanning(1),
		  .use_annotation(1'b0),
		  .vtrip(2'b10),
		  .width(1),
		  .ovt_hyst_trim(1'b0),
		  .ovt_needed(1'b0),
		  .ovt_slew_control(2'b00),
		  .input_buffer_sel(2'b00))
		Dm
		 (.oe(tmpOE__Dm_net),
		  .y({1'b0}),
		  .fb({tmpFB_0__Dm_net[0:0]}),
		  .analog({Net_597}),
		  .io({tmpIO_0__Dm_net[0:0]}),
		  .siovref(tmpSIOVREF__Dm_net),
		  .interrupt({tmpINTERRUPT_0__Dm_net[0:0]}),
		  .in_clock({1'b0}),
		  .in_clock_en({1'b1}),
		  .in_reset({1'b0}),
		  .out_clock({1'b0}),
		  .out_clock_en({1'b1}),
		  .out_reset({1'b0}));

	assign tmpOE__Dm_net = (`CYDEV_CHIP_MEMBER_USED == `CYDEV_CHIP_MEMBER_3A && `CYDEV_CHIP_REVISION_USED < `CYDEV_CHIP_REVISION_3A_ES3) ? ~{1'b1} : {1'b1};

	wire [0:0] tmpOE__Dp_net;
	wire [0:0] tmpFB_0__Dp_net;
	wire [0:0] tmpIO_0__Dp_net;
	electrical [0:0] tmpSIOVREF__Dp_net;

	cy_psoc3_pins_v1_10
		#(.id("beca5e2d-f70f-4900-a4db-7eca1ed3126e/618a72fc-5ddd-4df5-958f-a3d55102db42"),
		  .drive_mode(3'b000),
		  .ibuf_enabled(1'b0),
		  .init_dr_st(1'b1),
		  .input_clk_en(0),
		  .input_sync(1'b1),
		  .input_sync_mode(1'b0),
		  .intr_mode(2'b10),
		  .invert_in_clock(0),
		  .invert_in_clock_en(0),
		  .invert_in_reset(0),
		  .invert_out_clock(0),
		  .invert_out_clock_en(0),
		  .invert_out_reset(0),
		  .io_voltage(""),
		  .layout_mode("CONTIGUOUS"),
		  .oe_conn(1'b0),
		  .oe_reset(0),
		  .oe_sync(1'b0),
		  .output_clk_en(0),
		  .output_clock_mode(1'b0),
		  .output_conn(1'b0),
		  .output_mode(1'b0),
		  .output_reset(0),
		  .output_sync(1'b0),
		  .pa_in_clock(-1),
		  .pa_in_clock_en(-1),
		  .pa_in_reset(-1),
		  .pa_out_clock(-1),
		  .pa_out_clock_en(-1),
		  .pa_out_reset(-1),
		  .pin_aliases(""),
		  .pin_mode("I"),
		  .por_state(4),
		  .sio_group_cnt(0),
		  .sio_hyst(1'b1),
		  .sio_ibuf(""),
		  .sio_info(2'b00),
		  .sio_obuf(""),
		  .sio_refsel(""),
		  .sio_vtrip(""),
		  .sio_hifreq(""),
		  .sio_vohsel(""),
		  .slew_rate(1'b0),
		  .spanning(0),
		  .use_annotation(1'b0),
		  .vtrip(2'b00),
		  .width(1),
		  .ovt_hyst_trim(1'b0),
		  .ovt_needed(1'b0),
		  .ovt_slew_control(2'b00),
		  .input_buffer_sel(2'b00))
		Dp
		 (.oe(tmpOE__Dp_net),
		  .y({1'b0}),
		  .fb({tmpFB_0__Dp_net[0:0]}),
		  .analog({Net_1000}),
		  .io({tmpIO_0__Dp_net[0:0]}),
		  .siovref(tmpSIOVREF__Dp_net),
		  .interrupt({Net_1010}),
		  .in_clock({1'b0}),
		  .in_clock_en({1'b1}),
		  .in_reset({1'b0}),
		  .out_clock({1'b0}),
		  .out_clock_en({1'b1}),
		  .out_reset({1'b0}));

	assign tmpOE__Dp_net = (`CYDEV_CHIP_MEMBER_USED == `CYDEV_CHIP_MEMBER_3A && `CYDEV_CHIP_REVISION_USED < `CYDEV_CHIP_REVISION_3A_ES3) ? ~{1'b1} : {1'b1};

    cy_psoc3_usb_v1_0 USB (
        .dp(Net_1000),
        .dm(Net_597),
        .sof_int(sof),
        .arb_int(Net_1889),
        .usb_int(Net_1876),
        .ept_int(ep_int[8:0]),
        .ord_int(Net_95),
        .dma_req(dma_request[7:0]),
        .dma_termin(dma_terminate));


	cy_isr_v1_0
		#(.int_type(2'b10))
		ep_3
		 (.int_signal(ep_int[3]));



	cy_isr_v1_0
		#(.int_type(2'b10))
		ep_2
		 (.int_signal(ep_int[2]));



	cy_isr_v1_0
		#(.int_type(2'b10))
		ep_1
		 (.int_signal(ep_int[1]));



	cy_isr_v1_0
		#(.int_type(2'b10))
		ep_0
		 (.int_signal(ep_int[0]));



	cy_isr_v1_0
		#(.int_type(2'b10))
		bus_reset
		 (.int_signal(Net_1876));



	cy_isr_v1_0
		#(.int_type(2'b10))
		arb_int
		 (.int_signal(Net_1889));



	cy_isr_v1_0
		#(.int_type(2'b10))
		sof_int
		 (.int_signal(sof));


	// VirtualMux_1 (cy_virtualmux_v1_0)
	assign dma_complete[0] = Net_1922;

    ZeroTerminal ZeroTerminal_1 (
        .z(Net_1922));

	// VirtualMux_2 (cy_virtualmux_v1_0)
	assign dma_complete[1] = Net_1921;

    ZeroTerminal ZeroTerminal_2 (
        .z(Net_1921));

	// VirtualMux_3 (cy_virtualmux_v1_0)
	assign dma_complete[2] = Net_1920;

    ZeroTerminal ZeroTerminal_3 (
        .z(Net_1920));

	// VirtualMux_4 (cy_virtualmux_v1_0)
	assign dma_complete[3] = Net_1919;

    ZeroTerminal ZeroTerminal_4 (
        .z(Net_1919));

	// VirtualMux_5 (cy_virtualmux_v1_0)
	assign dma_complete[4] = Net_1918;

	// VirtualMux_6 (cy_virtualmux_v1_0)
	assign dma_complete[5] = Net_1917;

    ZeroTerminal ZeroTerminal_5 (
        .z(Net_1918));

    ZeroTerminal ZeroTerminal_6 (
        .z(Net_1917));

	// VirtualMux_7 (cy_virtualmux_v1_0)
	assign dma_complete[6] = Net_1916;

	// VirtualMux_8 (cy_virtualmux_v1_0)
	assign dma_complete[7] = Net_1915;

    ZeroTerminal ZeroTerminal_7 (
        .z(Net_1916));

    ZeroTerminal ZeroTerminal_8 (
        .z(Net_1915));



endmodule

// Component: cy_analog_virtualmux_v1_0
`ifdef CY_BLK_DIR
`undef CY_BLK_DIR
`endif

`ifdef WARP
`define CY_BLK_DIR "C:\Program Files (x86)\Cypress\PSoC Creator\4.1\PSoC Creator\psoc\content\CyPrimitives\cyprimitives.cylib\cy_analog_virtualmux_v1_0"
`include "C:\Program Files (x86)\Cypress\PSoC Creator\4.1\PSoC Creator\psoc\content\CyPrimitives\cyprimitives.cylib\cy_analog_virtualmux_v1_0\cy_analog_virtualmux_v1_0.v"
`else
`define CY_BLK_DIR "C:\Program Files (x86)\Cypress\PSoC Creator\4.1\PSoC Creator\psoc\content\CyPrimitives\cyprimitives.cylib\cy_analog_virtualmux_v1_0"
`include "C:\Program Files (x86)\Cypress\PSoC Creator\4.1\PSoC Creator\psoc\content\CyPrimitives\cyprimitives.cylib\cy_analog_virtualmux_v1_0\cy_analog_virtualmux_v1_0.v"
`endif

// Component: or_v1_0
`ifdef CY_BLK_DIR
`undef CY_BLK_DIR
`endif

`ifdef WARP
`define CY_BLK_DIR "C:\Program Files (x86)\Cypress\PSoC Creator\4.1\PSoC Creator\psoc\content\CyPrimitives\cyprimitives.cylib\or_v1_0"
`include "C:\Program Files (x86)\Cypress\PSoC Creator\4.1\PSoC Creator\psoc\content\CyPrimitives\cyprimitives.cylib\or_v1_0\or_v1_0.v"
`else
`define CY_BLK_DIR "C:\Program Files (x86)\Cypress\PSoC Creator\4.1\PSoC Creator\psoc\content\CyPrimitives\cyprimitives.cylib\or_v1_0"
`include "C:\Program Files (x86)\Cypress\PSoC Creator\4.1\PSoC Creator\psoc\content\CyPrimitives\cyprimitives.cylib\or_v1_0\or_v1_0.v"
`endif

// ADC_DelSig_v3_20(ADC_Alignment=0, ADC_Alignment_Config2=0, ADC_Alignment_Config3=0, ADC_Alignment_Config4=0, ADC_Charge_Pump_Clock=true, ADC_Clock=1, ADC_CLOCK_FREQUENCY=128000, ADC_Input_Mode=0, ADC_Input_Range=4, ADC_Input_Range_Config2=4, ADC_Input_Range_Config3=4, ADC_Input_Range_Config4=4, ADC_Power=1, ADC_Reference=0, ADC_Reference_Config2=0, ADC_Reference_Config3=0, ADC_Reference_Config4=0, ADC_Resolution=16, ADC_Resolution_Config2=16, ADC_Resolution_Config3=16, ADC_Resolution_Config4=16, Clock_Frequency=64000, Comment_Config1=Default Config, Comment_Config2=Second Config, Comment_Config3=Third Config, Comment_Config4=Fourth Config, Config1_Name=CFG1, Config2_Name=CFG2, Config3_Name=CFG3, Config4_Name=CFG4, Configs=4, Conversion_Mode=2, Conversion_Mode_Config2=2, Conversion_Mode_Config3=2, Conversion_Mode_Config4=2, Enable_Vref_Vss=false, EnableModulatorInput=false, Input_Buffer_Gain=1, Input_Buffer_Gain_Config2=1, Input_Buffer_Gain_Config3=1, Input_Buffer_Gain_Config4=1, Input_Buffer_Mode=1, Input_Buffer_Mode_Config2=1, Input_Buffer_Mode_Config3=1, Input_Buffer_Mode_Config4=1, Ref_Voltage=1.024, Ref_Voltage_Config2=1.024, Ref_Voltage_Config3=1.024, Ref_Voltage_Config4=1.024, rm_int=false, Sample_Rate=2000, Sample_Rate_Config2=10000, Sample_Rate_Config3=10000, Sample_Rate_Config4=10000, Start_of_Conversion=0, Vdda_Value=5, CY_API_CALLBACK_HEADER_INCLUDE=#include "cyapicallbacks.h", CY_COMMENT=, CY_COMPONENT_NAME=ADC_DelSig_v3_20, CY_CONST_CONFIG=true, CY_CONTROL_FILE=<:default:>, CY_DATASHEET_FILE=<:default:>, CY_FITTER_NAME=ADC_DelSig_1, CY_INSTANCE_SHORT_NAME=ADC_DelSig_1, CY_MAJOR_VERSION=3, CY_MINOR_VERSION=20, CY_PDL_DRIVER_NAME=, CY_PDL_DRIVER_REQ_VERSION=, CY_PDL_DRIVER_SUBGROUP=, CY_PDL_DRIVER_VARIANT=, CY_REMOVE=false, CY_SUPPRESS_API_GEN=false, CY_VERSION=PSoC Creator  4.1 Update 1, INSTANCE_NAME=ADC_DelSig_1, )
module ADC_DelSig_v3_20_1 (
    vplus,
    vminus,
    soc,
    eoc,
    aclk,
    nVref,
    mi);
    inout       vplus;
    electrical  vplus;
    inout       vminus;
    electrical  vminus;
    input       soc;
    output      eoc;
    input       aclk;
    inout       nVref;
    electrical  nVref;
    input       mi;


          wire  Net_268;
          wire  Net_270;
          wire  Net_252;
          wire  Net_275;
          wire  Net_250;
    electrical  Net_249;
    electrical  Net_257;
    electrical  Net_248;
    electrical  Net_23;
          wire  Net_247;
          wire  aclock;
          wire [3:0] mod_dat;
          wire  mod_reset;
    electrical  Net_352;
          wire  Net_246;
          wire [7:0] Net_245;
          wire  Net_482;
    electrical  Net_34;
    electrical  Net_35;
    electrical  Net_244;
          wire  Net_93;
    electrical  Net_20;
    electrical  Net_690;
    electrical  Net_686;
    electrical  Net_520;
          wire  Net_481;
    electrical  Net_677;
    electrical  Net_41;
    electrical  Net_573;
    electrical  Net_109;
          wire  Net_488;

	// cy_analog_virtualmux_6 (cy_analog_virtualmux_v1_0)
	cy_connect_v1_0 cy_analog_virtualmux_6_connect(Net_690, Net_35);
	defparam cy_analog_virtualmux_6_connect.sig_width = 1;

    cy_analog_noconnect_v1_0 cy_analog_noconnect_1 (
        .noconnect(Net_34));

	// cy_analog_virtualmux_4 (cy_analog_virtualmux_v1_0)
	cy_connect_v1_0 cy_analog_virtualmux_4_connect(Net_677, Net_34);
	defparam cy_analog_virtualmux_4_connect.sig_width = 1;

    cy_psoc3_ds_mod_v4_0 DSM (
        .vplus(vplus),
        .vminus(Net_520),
        .modbit(Net_481),
        .reset_udb(Net_482),
        .aclock(Net_488),
        .mod_dat(mod_dat[3:0]),
        .dout_udb(Net_245[7:0]),
        .reset_dec(mod_reset),
        .dec_clock(aclock),
        .extclk_cp_udb(Net_93),
        .clk_udb(1'b0),
        .ext_pin_1(Net_573),
        .ext_pin_2(Net_41),
        .ext_vssa(Net_109),
        .qtz_ref(Net_677));
    defparam DSM.resolution = 16;

    cy_analog_noconnect_v1_0 cy_analog_noconnect_5 (
        .noconnect(Net_352));

	// cy_analog_virtualmux_5 (cy_analog_virtualmux_v1_0)
	cy_connect_v1_0 cy_analog_virtualmux_5_connect(Net_109, Net_352);
	defparam cy_analog_virtualmux_5_connect.sig_width = 1;


	cy_clock_v1_0
		#(.id("8bda02ab-ec76-474b-8a67-a1480733cde5/b7604721-db56-4477-98c2-8fae77869066"),
		  .source_clock_id("61737EF6-3B74-48f9-8B91-F7473A442AE7"),
		  .divisor(1),
		  .period("0"),
		  .is_direct(0),
		  .is_digital(1))
		Ext_CP_Clk
		 (.clock_out(Net_93));


    cy_analog_noconnect_v1_0 cy_analog_noconnect_3 (
        .noconnect(Net_257));

    cy_analog_noconnect_v1_0 cy_analog_noconnect_2 (
        .noconnect(Net_249));

	// cy_analog_virtualmux_3 (cy_analog_virtualmux_v1_0)
	cy_connect_v1_0 cy_analog_virtualmux_3_connect(Net_41, Net_257);
	defparam cy_analog_virtualmux_3_connect.sig_width = 1;

	// cy_analog_virtualmux_2 (cy_analog_virtualmux_v1_0)
	cy_connect_v1_0 cy_analog_virtualmux_2_connect(Net_573, Net_249);
	defparam cy_analog_virtualmux_2_connect.sig_width = 1;

	// cy_analog_virtualmux_1 (cy_analog_virtualmux_v1_0)
	cy_connect_v1_0 cy_analog_virtualmux_1_connect(Net_520, vminus);
	defparam cy_analog_virtualmux_1_connect.sig_width = 1;


	cy_isr_v1_0
		#(.int_type(2'b10))
		IRQ
		 (.int_signal(eoc));


	// Clock_VirtualMux (cy_virtualmux_v1_0)
	assign Net_488 = Net_250;


	cy_clock_v1_0
		#(.id("8bda02ab-ec76-474b-8a67-a1480733cde5/edd15f43-b66b-457b-be3a-5342345270c8"),
		  .source_clock_id("61737EF6-3B74-48f9-8B91-F7473A442AE7"),
		  .divisor(0),
		  .period("7812500000"),
		  .is_direct(0),
		  .is_digital(0))
		theACLK
		 (.clock_out(Net_250));


    ZeroTerminal ZeroTerminal_2 (
        .z(Net_482));

	// Clock_VirtualMux_1 (cy_virtualmux_v1_0)
	assign Net_481 = Net_252;

    cy_psoc3_decimator_v1_0 DEC (
        .aclock(aclock),
        .mod_dat(mod_dat[3:0]),
        .ext_start(soc),
        .mod_reset(mod_reset),
        .interrupt(eoc));

    ZeroTerminal ZeroTerminal_1 (
        .z(Net_252));


    assign Net_268 = Net_270 | Net_93;

    ZeroTerminal ZeroTerminal_3 (
        .z(Net_270));



endmodule

// TIA_v2_0(Capacitive_Feedback=3, Fcorner=35 kHz, Power=2, Resistive_Feedback=7, vdda_value=5, CY_API_CALLBACK_HEADER_INCLUDE=#include "cyapicallbacks.h", CY_COMMENT=, CY_COMPONENT_NAME=TIA_v2_0, CY_CONST_CONFIG=true, CY_CONTROL_FILE=<:default:>, CY_DATASHEET_FILE=<:default:>, CY_FITTER_NAME=TIA_1, CY_INSTANCE_SHORT_NAME=TIA_1, CY_MAJOR_VERSION=2, CY_MINOR_VERSION=0, CY_PDL_DRIVER_NAME=, CY_PDL_DRIVER_REQ_VERSION=, CY_PDL_DRIVER_SUBGROUP=, CY_PDL_DRIVER_VARIANT=, CY_REMOVE=false, CY_SUPPRESS_API_GEN=false, CY_VERSION=PSoC Creator  4.1 Update 1, INSTANCE_NAME=TIA_1, )
module TIA_v2_0_2 (
    Iin,
    Vref,
    Vout);
    inout       Iin;
    electrical  Iin;
    inout       Vref;
    electrical  Vref;
    inout       Vout;
    electrical  Vout;


          wire  Net_60;
          wire  Net_52;
          wire  Net_39;
          wire  Net_38;
          wire  Net_37;

    cy_psoc3_scblock_v1_0 SC (
        .vin(Iin),
        .vref(Vref),
        .vout(Vout),
        .modout_sync(Net_60),
        .aclk(Net_37),
        .clk_udb(Net_38),
        .dyn_cntl(Net_39),
        .bst_clk(Net_52));

    ZeroTerminal ZeroTerminal_1 (
        .z(Net_37));

    ZeroTerminal ZeroTerminal_2 (
        .z(Net_38));

    ZeroTerminal ZeroTerminal_3 (
        .z(Net_39));

    ZeroTerminal ZeroTerminal_4 (
        .z(Net_52));



endmodule

// VDAC8_v1_90(Data_Source=0, Initial_Value=0, Strobe_Mode=0, VDAC_Range=4, VDAC_Speed=0, Voltage=0, CY_API_CALLBACK_HEADER_INCLUDE=#include "cyapicallbacks.h", CY_COMMENT=, CY_COMPONENT_NAME=VDAC8_v1_90, CY_CONST_CONFIG=true, CY_CONTROL_FILE=<:default:>, CY_DATASHEET_FILE=<:default:>, CY_FITTER_NAME=VDAC_Vgs, CY_INSTANCE_SHORT_NAME=VDAC_Vgs, CY_MAJOR_VERSION=1, CY_MINOR_VERSION=90, CY_PDL_DRIVER_NAME=, CY_PDL_DRIVER_REQ_VERSION=, CY_PDL_DRIVER_SUBGROUP=, CY_PDL_DRIVER_VARIANT=, CY_REMOVE=false, CY_SUPPRESS_API_GEN=false, CY_VERSION=PSoC Creator  4.1 Update 1, INSTANCE_NAME=VDAC_Vgs, )
module VDAC8_v1_90_3 (
    strobe,
    data,
    vOut);
    input       strobe;
    input      [7:0] data;
    inout       vOut;
    electrical  vOut;

    parameter Data_Source = 0;
    parameter Initial_Value = 0;
    parameter Strobe_Mode = 0;

    electrical  Net_77;
          wire  Net_83;
          wire  Net_82;
          wire  Net_81;

    cy_psoc3_vidac8_v1_0 viDAC8 (
        .reset(Net_83),
        .idir(Net_81),
        .data(data[7:0]),
        .strobe(strobe),
        .vout(vOut),
        .iout(Net_77),
        .ioff(Net_82),
        .strobe_udb(strobe));
    defparam viDAC8.is_all_if_any = 0;
    defparam viDAC8.reg_data = 0;

    ZeroTerminal ZeroTerminal_1 (
        .z(Net_81));

    ZeroTerminal ZeroTerminal_2 (
        .z(Net_82));

    ZeroTerminal ZeroTerminal_3 (
        .z(Net_83));

    cy_analog_noconnect_v1_0 cy_analog_noconnect_1 (
        .noconnect(Net_77));



endmodule

// VDAC8_v1_90(Data_Source=0, Initial_Value=125, Strobe_Mode=0, VDAC_Range=0, VDAC_Speed=0, Voltage=500, CY_API_CALLBACK_HEADER_INCLUDE=#include "cyapicallbacks.h", CY_COMMENT=, CY_COMPONENT_NAME=VDAC8_v1_90, CY_CONST_CONFIG=true, CY_CONTROL_FILE=<:default:>, CY_DATASHEET_FILE=<:default:>, CY_FITTER_NAME=VDAC_Vds, CY_INSTANCE_SHORT_NAME=VDAC_Vds, CY_MAJOR_VERSION=1, CY_MINOR_VERSION=90, CY_PDL_DRIVER_NAME=, CY_PDL_DRIVER_REQ_VERSION=, CY_PDL_DRIVER_SUBGROUP=, CY_PDL_DRIVER_VARIANT=, CY_REMOVE=false, CY_SUPPRESS_API_GEN=false, CY_VERSION=PSoC Creator  4.1 Update 1, INSTANCE_NAME=VDAC_Vds, )
module VDAC8_v1_90_4 (
    strobe,
    data,
    vOut);
    input       strobe;
    input      [7:0] data;
    inout       vOut;
    electrical  vOut;

    parameter Data_Source = 0;
    parameter Initial_Value = 125;
    parameter Strobe_Mode = 0;

    electrical  Net_77;
          wire  Net_83;
          wire  Net_82;
          wire  Net_81;

    cy_psoc3_vidac8_v1_0 viDAC8 (
        .reset(Net_83),
        .idir(Net_81),
        .data(data[7:0]),
        .strobe(strobe),
        .vout(vOut),
        .iout(Net_77),
        .ioff(Net_82),
        .strobe_udb(strobe));
    defparam viDAC8.is_all_if_any = 0;
    defparam viDAC8.reg_data = 0;

    ZeroTerminal ZeroTerminal_1 (
        .z(Net_81));

    ZeroTerminal ZeroTerminal_2 (
        .z(Net_82));

    ZeroTerminal ZeroTerminal_3 (
        .z(Net_83));

    cy_analog_noconnect_v1_0 cy_analog_noconnect_1 (
        .noconnect(Net_77));



endmodule

// VDAC8_v1_90(Data_Source=0, Initial_Value=125, Strobe_Mode=0, VDAC_Range=4, VDAC_Speed=0, Voltage=2000, CY_API_CALLBACK_HEADER_INCLUDE=#include "cyapicallbacks.h", CY_COMMENT=, CY_COMPONENT_NAME=VDAC8_v1_90, CY_CONST_CONFIG=true, CY_CONTROL_FILE=<:default:>, CY_DATASHEET_FILE=<:default:>, CY_FITTER_NAME=VDAC_Ref, CY_INSTANCE_SHORT_NAME=VDAC_Ref, CY_MAJOR_VERSION=1, CY_MINOR_VERSION=90, CY_PDL_DRIVER_NAME=, CY_PDL_DRIVER_REQ_VERSION=, CY_PDL_DRIVER_SUBGROUP=, CY_PDL_DRIVER_VARIANT=, CY_REMOVE=false, CY_SUPPRESS_API_GEN=false, CY_VERSION=PSoC Creator  4.1 Update 1, INSTANCE_NAME=VDAC_Ref, )
module VDAC8_v1_90_5 (
    strobe,
    data,
    vOut);
    input       strobe;
    input      [7:0] data;
    inout       vOut;
    electrical  vOut;

    parameter Data_Source = 0;
    parameter Initial_Value = 125;
    parameter Strobe_Mode = 0;

    electrical  Net_77;
          wire  Net_83;
          wire  Net_82;
          wire  Net_81;

    cy_psoc3_vidac8_v1_0 viDAC8 (
        .reset(Net_83),
        .idir(Net_81),
        .data(data[7:0]),
        .strobe(strobe),
        .vout(vOut),
        .iout(Net_77),
        .ioff(Net_82),
        .strobe_udb(strobe));
    defparam viDAC8.is_all_if_any = 0;
    defparam viDAC8.reg_data = 0;

    ZeroTerminal ZeroTerminal_1 (
        .z(Net_81));

    ZeroTerminal ZeroTerminal_2 (
        .z(Net_82));

    ZeroTerminal ZeroTerminal_3 (
        .z(Net_83));

    cy_analog_noconnect_v1_0 cy_analog_noconnect_1 (
        .noconnect(Net_77));



endmodule

// top
module top ;

          wire [7:0] Net_37;
          wire  Net_36;
    electrical  Net_35;
          wire [7:0] Net_33;
          wire  Net_32;
    electrical  Net_31;
          wire [7:0] Net_29;
          wire  Net_28;
    electrical  Net_25;
          wire  Net_24;
    electrical  Net_23;
          wire  Net_22;
          wire  Net_21;
          wire  Net_20;
          wire  Net_17;
          wire  Net_16;
    electrical  Net_26;
    electrical  Net_27;

    USBFS_v3_20_0 USBUART (
        .sof(Net_16),
        .vbusdet(1'b0));
    defparam USBUART.epDMAautoOptimization = 0;

    ADC_DelSig_v3_20_1 ADC_DelSig_1 (
        .vplus(Net_27),
        .vminus(Net_26),
        .soc(1'b1),
        .eoc(Net_21),
        .aclk(1'b0),
        .nVref(Net_23),
        .mi(1'b0));

    TIA_v2_0_2 TIA_1 (
        .Iin(Net_25),
        .Vref(Net_26),
        .Vout(Net_27));

    VDAC8_v1_90_3 VDAC_Vgs (
        .strobe(1'b0),
        .data(8'b00000000),
        .vOut(Net_31));
    defparam VDAC_Vgs.Data_Source = 0;
    defparam VDAC_Vgs.Initial_Value = 0;
    defparam VDAC_Vgs.Strobe_Mode = 0;

	wire [0:0] tmpOE__Pin_Vgs_net;
	wire [0:0] tmpFB_0__Pin_Vgs_net;
	wire [0:0] tmpIO_0__Pin_Vgs_net;
	wire [0:0] tmpINTERRUPT_0__Pin_Vgs_net;
	electrical [0:0] tmpSIOVREF__Pin_Vgs_net;

	cy_psoc3_pins_v1_10
		#(.id("77715107-f8d5-47e5-a629-0fb83101ac6b"),
		  .drive_mode(3'b000),
		  .ibuf_enabled(1'b0),
		  .init_dr_st(1'b0),
		  .input_clk_en(0),
		  .input_sync(1'b1),
		  .input_sync_mode(1'b0),
		  .intr_mode(2'b00),
		  .invert_in_clock(0),
		  .invert_in_clock_en(0),
		  .invert_in_reset(0),
		  .invert_out_clock(0),
		  .invert_out_clock_en(0),
		  .invert_out_reset(0),
		  .io_voltage(""),
		  .layout_mode("CONTIGUOUS"),
		  .oe_conn(1'b0),
		  .oe_reset(0),
		  .oe_sync(1'b0),
		  .output_clk_en(0),
		  .output_clock_mode(1'b0),
		  .output_conn(1'b0),
		  .output_mode(1'b0),
		  .output_reset(0),
		  .output_sync(1'b0),
		  .pa_in_clock(-1),
		  .pa_in_clock_en(-1),
		  .pa_in_reset(-1),
		  .pa_out_clock(-1),
		  .pa_out_clock_en(-1),
		  .pa_out_reset(-1),
		  .pin_aliases(""),
		  .pin_mode("A"),
		  .por_state(4),
		  .sio_group_cnt(0),
		  .sio_hyst(1'b1),
		  .sio_ibuf(""),
		  .sio_info(2'b00),
		  .sio_obuf(""),
		  .sio_refsel(""),
		  .sio_vtrip(""),
		  .sio_hifreq(""),
		  .sio_vohsel(""),
		  .slew_rate(1'b0),
		  .spanning(0),
		  .use_annotation(1'b0),
		  .vtrip(2'b10),
		  .width(1),
		  .ovt_hyst_trim(1'b0),
		  .ovt_needed(1'b0),
		  .ovt_slew_control(2'b00),
		  .input_buffer_sel(2'b00))
		Pin_Vgs
		 (.oe(tmpOE__Pin_Vgs_net),
		  .y({1'b0}),
		  .fb({tmpFB_0__Pin_Vgs_net[0:0]}),
		  .analog({Net_31}),
		  .io({tmpIO_0__Pin_Vgs_net[0:0]}),
		  .siovref(tmpSIOVREF__Pin_Vgs_net),
		  .interrupt({tmpINTERRUPT_0__Pin_Vgs_net[0:0]}),
		  .in_clock({1'b0}),
		  .in_clock_en({1'b1}),
		  .in_reset({1'b0}),
		  .out_clock({1'b0}),
		  .out_clock_en({1'b1}),
		  .out_reset({1'b0}));

	assign tmpOE__Pin_Vgs_net = (`CYDEV_CHIP_MEMBER_USED == `CYDEV_CHIP_MEMBER_3A && `CYDEV_CHIP_REVISION_USED < `CYDEV_CHIP_REVISION_3A_ES3) ? ~{1'b1} : {1'b1};

    VDAC8_v1_90_4 VDAC_Vds (
        .strobe(1'b0),
        .data(8'b00000000),
        .vOut(Net_35));
    defparam VDAC_Vds.Data_Source = 0;
    defparam VDAC_Vds.Initial_Value = 125;
    defparam VDAC_Vds.Strobe_Mode = 0;

	wire [0:0] tmpOE__Pin_Vds_net;
	wire [0:0] tmpFB_0__Pin_Vds_net;
	wire [0:0] tmpIO_0__Pin_Vds_net;
	wire [0:0] tmpINTERRUPT_0__Pin_Vds_net;
	electrical [0:0] tmpSIOVREF__Pin_Vds_net;

	cy_psoc3_pins_v1_10
		#(.id("5d768a13-20b3-45d1-9ce6-fe7b2c158df4"),
		  .drive_mode(3'b000),
		  .ibuf_enabled(1'b0),
		  .init_dr_st(1'b0),
		  .input_clk_en(0),
		  .input_sync(1'b1),
		  .input_sync_mode(1'b0),
		  .intr_mode(2'b00),
		  .invert_in_clock(0),
		  .invert_in_clock_en(0),
		  .invert_in_reset(0),
		  .invert_out_clock(0),
		  .invert_out_clock_en(0),
		  .invert_out_reset(0),
		  .io_voltage(""),
		  .layout_mode("CONTIGUOUS"),
		  .oe_conn(1'b0),
		  .oe_reset(0),
		  .oe_sync(1'b0),
		  .output_clk_en(0),
		  .output_clock_mode(1'b0),
		  .output_conn(1'b0),
		  .output_mode(1'b0),
		  .output_reset(0),
		  .output_sync(1'b0),
		  .pa_in_clock(-1),
		  .pa_in_clock_en(-1),
		  .pa_in_reset(-1),
		  .pa_out_clock(-1),
		  .pa_out_clock_en(-1),
		  .pa_out_reset(-1),
		  .pin_aliases(""),
		  .pin_mode("A"),
		  .por_state(4),
		  .sio_group_cnt(0),
		  .sio_hyst(1'b1),
		  .sio_ibuf(""),
		  .sio_info(2'b00),
		  .sio_obuf(""),
		  .sio_refsel(""),
		  .sio_vtrip(""),
		  .sio_hifreq(""),
		  .sio_vohsel(""),
		  .slew_rate(1'b0),
		  .spanning(0),
		  .use_annotation(1'b0),
		  .vtrip(2'b10),
		  .width(1),
		  .ovt_hyst_trim(1'b0),
		  .ovt_needed(1'b0),
		  .ovt_slew_control(2'b00),
		  .input_buffer_sel(2'b00))
		Pin_Vds
		 (.oe(tmpOE__Pin_Vds_net),
		  .y({1'b0}),
		  .fb({tmpFB_0__Pin_Vds_net[0:0]}),
		  .analog({Net_35}),
		  .io({tmpIO_0__Pin_Vds_net[0:0]}),
		  .siovref(tmpSIOVREF__Pin_Vds_net),
		  .interrupt({tmpINTERRUPT_0__Pin_Vds_net[0:0]}),
		  .in_clock({1'b0}),
		  .in_clock_en({1'b1}),
		  .in_reset({1'b0}),
		  .out_clock({1'b0}),
		  .out_clock_en({1'b1}),
		  .out_reset({1'b0}));

	assign tmpOE__Pin_Vds_net = (`CYDEV_CHIP_MEMBER_USED == `CYDEV_CHIP_MEMBER_3A && `CYDEV_CHIP_REVISION_USED < `CYDEV_CHIP_REVISION_3A_ES3) ? ~{1'b1} : {1'b1};

	wire [0:0] tmpOE__Pin_Vss_net;
	wire [0:0] tmpFB_0__Pin_Vss_net;
	wire [0:0] tmpIO_0__Pin_Vss_net;
	wire [0:0] tmpINTERRUPT_0__Pin_Vss_net;
	electrical [0:0] tmpSIOVREF__Pin_Vss_net;

	cy_psoc3_pins_v1_10
		#(.id("d897ddac-8ddf-4a56-9992-12b9a6662dce"),
		  .drive_mode(3'b000),
		  .ibuf_enabled(1'b0),
		  .init_dr_st(1'b0),
		  .input_clk_en(0),
		  .input_sync(1'b1),
		  .input_sync_mode(1'b0),
		  .intr_mode(2'b00),
		  .invert_in_clock(0),
		  .invert_in_clock_en(0),
		  .invert_in_reset(0),
		  .invert_out_clock(0),
		  .invert_out_clock_en(0),
		  .invert_out_reset(0),
		  .io_voltage(""),
		  .layout_mode("CONTIGUOUS"),
		  .oe_conn(1'b0),
		  .oe_reset(0),
		  .oe_sync(1'b0),
		  .output_clk_en(0),
		  .output_clock_mode(1'b0),
		  .output_conn(1'b0),
		  .output_mode(1'b0),
		  .output_reset(0),
		  .output_sync(1'b0),
		  .pa_in_clock(-1),
		  .pa_in_clock_en(-1),
		  .pa_in_reset(-1),
		  .pa_out_clock(-1),
		  .pa_out_clock_en(-1),
		  .pa_out_reset(-1),
		  .pin_aliases(""),
		  .pin_mode("A"),
		  .por_state(4),
		  .sio_group_cnt(0),
		  .sio_hyst(1'b1),
		  .sio_ibuf(""),
		  .sio_info(2'b00),
		  .sio_obuf(""),
		  .sio_refsel(""),
		  .sio_vtrip(""),
		  .sio_hifreq(""),
		  .sio_vohsel(""),
		  .slew_rate(1'b0),
		  .spanning(0),
		  .use_annotation(1'b0),
		  .vtrip(2'b10),
		  .width(1),
		  .ovt_hyst_trim(1'b0),
		  .ovt_needed(1'b0),
		  .ovt_slew_control(2'b00),
		  .input_buffer_sel(2'b00))
		Pin_Vss
		 (.oe(tmpOE__Pin_Vss_net),
		  .y({1'b0}),
		  .fb({tmpFB_0__Pin_Vss_net[0:0]}),
		  .analog({Net_25}),
		  .io({tmpIO_0__Pin_Vss_net[0:0]}),
		  .siovref(tmpSIOVREF__Pin_Vss_net),
		  .interrupt({tmpINTERRUPT_0__Pin_Vss_net[0:0]}),
		  .in_clock({1'b0}),
		  .in_clock_en({1'b1}),
		  .in_reset({1'b0}),
		  .out_clock({1'b0}),
		  .out_clock_en({1'b1}),
		  .out_reset({1'b0}));

	assign tmpOE__Pin_Vss_net = (`CYDEV_CHIP_MEMBER_USED == `CYDEV_CHIP_MEMBER_3A && `CYDEV_CHIP_REVISION_USED < `CYDEV_CHIP_REVISION_3A_ES3) ? ~{1'b1} : {1'b1};

    VDAC8_v1_90_5 VDAC_Ref (
        .strobe(1'b0),
        .data(8'b00000000),
        .vOut(Net_26));
    defparam VDAC_Ref.Data_Source = 0;
    defparam VDAC_Ref.Initial_Value = 125;
    defparam VDAC_Ref.Strobe_Mode = 0;



endmodule

