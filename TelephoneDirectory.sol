// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;
contract People {
    string name;
    uint256 number;
    address owner;

    constructor (address _owner) public {
        owner = _owner;
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    } 

    function set_name (string memory _name) public onlyOwner {
        name = _name;
    }

    function set_number (uint256 _number) public onlyOwner {
        number = _number;
    }

    function get_name() public view onlyOwner returns (string memory) {
        return name;
    }

    function get_number() public view onlyOwner returns (uint256) {
        return number;
    }
}

contract TelephoneDirectory {

    People[] public people;
    uint256 private peopleIndex = 0;
    mapping(address => uint256) public address_to_idx;

    function add_people(string memory name, uint256 number) public {
        People p = new People(address(msg.sender));
        p.set_name(name);
        p.set_number(number);
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