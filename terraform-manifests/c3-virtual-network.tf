resource "azurerm_virtual_network" "vnet" {
	name = "vnet-1"
	address_space = ["10.0.0.0/16"]
	location = azurerm_resource_group.rg-1.location
	resource_group_name = azurerm_resource_group.rg-1.name
	tags = {
		"Env" = "Dev"
	}
}
resource "azurerm_subnet" "subnet" {
	name = "subnet"
	resource_group_name = azurerm_resource_group.rg-1.name
	virtual_network_name = azurerm_virtual_network.vnet.name
	address_prefixes = ["10.0.2.0/24"]
}
resource "azurerm_public_ip" "publicip" {
	name = "publicip"
	resource_group_name = azurerm_resource_group.rg-1.name
	location = azurerm_resource_group.rg-1.location
	allocation_method = "Static"
	tags = {
		environment = "Dev"
	}
}
resource "azurerm_network_interface" "vmnic" {
	name = "vmnic"
	location = azurerm_resource_group.rg-1.location
	resource_group_name = azurerm_resource_group.rg-1.name
	ip_configuration {
		name = "internal"
		subnet_id = azurerm_subnet.subnet.id
		private_ip_address_allocation = "Dynamic"
		public_ip_address_id = azurerm_public_ip.publicip.id
	}
}