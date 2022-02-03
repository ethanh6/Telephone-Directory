// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;
contract People {
    string name;
    uint256 number;
    address owner;

    constructor (string memory _name, uint256 _number) public {
        owner = msg.sender;
        name = _name;
        number = _number;
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    } 

    function set_name (string memory _name) onlyOwner public {
        name = _name;
    }

    function set_number (uint256 _number) onlyOwner public {
        number = _number;
    }

    function get_name() public view returns (string memory) {
        return name;
    }

    function get_number() public view returns (uint256) {
        return number;
    }
}

contract TelephoneDirectory {

    People[] public people;
    uint256 private peopleIndex = 0;
    mapping(address => uint256) public address_to_idx;

    function add_people(string memory name, uint256 number) public {
        People p = new People(name, number);
        people.push(p);
        address_to_idx[msg.sender] = peopleIndex;
        peopleIndex ++;
    }

    function get_total_people_number() public view returns(uint256){
        return peopleIndex;
    }
    
    function get_info() public view returns (string memory, uint256){
        address addr = address(msg.sender);
        string memory name = people[address_to_idx[addr]].get_name();
        uint256 number = people[address_to_idx[addr]].get_number();
        return (name, number);
    }

    function set_info(string memory _name, uint256 _number) public {
        address addr = address(msg.sender);
        people[address_to_idx[addr]].set_number(_number);
        people[address_to_idx[addr]].set_name(_name);
    }

}