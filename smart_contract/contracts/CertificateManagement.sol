// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CertificateManagement {
    struct CertificateCreation {
        uint256 id;
        address carrier;
        address recipient;  // Main owner
        address broker;  // Main owner
        mapping(address => bool) nominees;  // Updated to mapping
        mapping(uint256 => Change) changes; // Map change ID to Change struct
        uint256 changesCount; // Counter for tracking changes
        string data;
        bool isFinalized;
        bool isActive;
        uint256 manufacturingDate;
        uint256 expiryDate;
    }

    mapping (uint256 => address) public expireCertificates;

    struct Change {
        uint256 changeId;
        uint256 fieldID;
        address initiatorNominee;
        string updatedData;
        bool updatedByOwner;
        bool updatedByBroker;
        bool updatedByIndustry;
        bool reject;
    }

    mapping (uint256 => address[]) public owners;

    mapping(uint256 => CertificateCreation) public certificates;

    mapping(address => string) public roles;
    
    address mainIndustry = 0x28C4ecE44829584941E5db3D6F2cCB304B173a78;
    constructor(){
        roles[mainIndustry] = "industry";
    }

    uint256 public nextCertificateId;
    uint256 public tempCount = 0;

    // broker will create the certificate
    function createCertificate(
        address _owner,
        address _broker,
        string memory _data,
        uint256 _manufacturingDate,
        uint256 _expiryDate
    ) public payable {
        require(keccak256(abi.encodePacked(roles[_broker])) == keccak256(abi.encodePacked("broker")) , "You are not a Broker");
        require(keccak256(abi.encodePacked(roles[_owner])) == keccak256(abi.encodePacked("client")) , "Not a valid Client");
        uint256 newId = nextCertificateId;
        CertificateCreation storage newCertificate = certificates[newId];
        newCertificate.id = newId;
        newCertificate.carrier = mainIndustry;
        newCertificate.recipient = _owner;
        newCertificate.broker = _broker;
        newCertificate.nominees[mainIndustry] = true;
        newCertificate.nominees[_owner] = true;
        newCertificate.nominees[_broker] = true;
        newCertificate.data = _data;
        newCertificate.isFinalized = true;
        newCertificate.isActive = true;
        newCertificate.manufacturingDate = _manufacturingDate;
        newCertificate.expiryDate = _expiryDate;
        
        owners[newId].push(_owner); 
        
        nextCertificateId+=1;
    }

    function requestChanges(uint256 _id, uint256 _fieldId, string memory _updatedData, address _nominee) public {
        require(_id < nextCertificateId, "Certificate does not exist");
        CertificateCreation storage cert = certificates[_id];
        require(cert.isActive, "Certificate is not active");
        require(cert.nominees[_nominee], "You dont have this right");
        Change storage newChange = cert.changes[cert.changesCount];
        newChange.changeId = cert.changesCount;
        newChange.fieldID = _fieldId;
        newChange.initiatorNominee = _nominee;
        newChange.updatedData = _updatedData;
        newChange.updatedByOwner = false;
        newChange.updatedByBroker = false;
        newChange.updatedByIndustry = false;
        newChange.reject = false;
        cert.changesCount+=1;
    }

    function rejectChanges(uint256 _id,uint256 _changeId) public {
        require(_id < nextCertificateId, "Certificate does not exist");
        CertificateCreation storage cert = certificates[_id];
        require(cert.isActive, "Certificate is not active");
        require(_changeId < cert.changesCount, "Invalid change ID");
        Change storage change = cert.changes[_changeId];
        change.updatedByOwner = false;
        change.updatedByBroker = false;
        change.updatedByIndustry = false;
        change.reject = true;
    }

    function approveChangesByOwner(uint256 _id,uint256 _changeId, address _owner) public {
        require(_id < nextCertificateId, "Certificate does not exist");
        CertificateCreation storage cert = certificates[_id];
        require(cert.isActive, "Certificate is not active");
        require(_owner == cert.recipient, "You are not the Owner for this Policy");
        require(_changeId < cert.changesCount, "Invalid change ID");
        Change storage change = cert.changes[_changeId];
        change.updatedByOwner = true;
    }
    
    function approveChangesByBroker(uint256 _id,uint256 _changeId, address _broker) public {
        require(_id < nextCertificateId, "Certificate does not exist");
        CertificateCreation storage cert = certificates[_id];
        require(cert.isActive, "Certificate is not active");
        require(_broker == cert.broker, "You are not the Broker for this Policy");
        require(_changeId < cert.changesCount, "Invalid change ID");
        Change storage change = cert.changes[_changeId];
        change.updatedByBroker = true;
    }

    // Function to approve changes to a certificate
    function approveChangesByIndustry(uint256 _id, uint256 _changeId, address industry) public {
        require(_id < nextCertificateId, "Certificate does not exist");
        CertificateCreation storage cert = certificates[_id];
        require(cert.isActive, "Certificate is not active");
        require(industry == mainIndustry, "You are not the Industry");
        // Ensure the change ID is valid
        require(_changeId < cert.changesCount, "Invalid change ID");
        Change storage change = cert.changes[_changeId];
        require(change.updatedByOwner && change.updatedByBroker, "Yet Not Verified by supporting Parties");
        // Approve the change
        change.updatedByIndustry = true;
        cert.data = change.updatedData;
    }

    // Function to transfer ownership to another address
    function transferOwnership(uint256 _id, address _newOwner, address _current) public {
        require(_id < nextCertificateId, "Certificate does not exist");
        CertificateCreation storage cert = certificates[_id];
        require(cert.isActive, "Certificate is not active");
        require(_current != cert.recipient, "You are not owner of this certificate");
        require(_current != _newOwner, "Same person no changes");
        require(_current != cert.broker && _current != cert.carrier , "Only owner can transfer ownership");
        // Remove the current owner as the carrier and add the new owner
        cert.recipient = _newOwner;
        roles[_newOwner] = "client";
        owners[_id].push(_newOwner); 

    }

    // Function to add a nominee
    function addNominee(uint256 _id, address _nominee, address _owner) public {
        require(_id < nextCertificateId, "Certificate does not exist");
        CertificateCreation storage cert = certificates[_id];
        require(cert.isActive, "Certificate is not active");
        require(cert.recipient == _owner, "Only the main owner can add nominees");
        // Add the nominee to the nominees mapping
        cert.nominees[_nominee] = true;
    }

    // Function to remove a nominee
    function removeNominee(uint256 _id, address _nominee, address _owner) public {
        require(_id < nextCertificateId, "Certificate does not exist");
        CertificateCreation storage cert = certificates[_id];
        require(cert.isActive, "Certificate is not active");
        require(cert.recipient == _owner, "Only the main owner can remove nominees");
        require(cert.nominees[_nominee], "This person in not in nominee list");
        require(_nominee!=cert.carrier && _nominee!=cert.broker && _nominee!=cert.recipient, "You can't remove them from the list");
        // Remove the nominee from the nominees mapping
        delete cert.nominees[_nominee];
    }

    // Function to retrieve certificate details
    function getCertificateDetails(uint256 _id) public view returns (address, address, address, uint256, string memory, bool, bool, uint256, uint256) {
        require(_id < nextCertificateId, "Certificate does not exist");
        CertificateCreation storage cert = certificates[_id];
        return (cert.carrier, cert.recipient, cert.broker, cert.changesCount, cert.data, cert.isActive, cert.isFinalized, cert.manufacturingDate, cert.expiryDate);
    }

    // Function to make request to delete certificate
    function deleteRequest(uint256 _id, address _address) public {
        require(_id < nextCertificateId, "Certificate does not exist");
        CertificateCreation storage cert = certificates[_id];
        require(cert.isActive, "Certificate is not active");
        address addressRequesting = expireCertificates[_id];
        require(addressRequesting==cert.broker || addressRequesting==cert.recipient || addressRequesting==cert.carrier, "You have no right to make delete request");
        expireCertificates[_id] = _address;
    } 

    // delete certificate by industry
    function deleteCertificate(uint256 _id, address _industry) public {
        require(_id < nextCertificateId, "Certificate does not exist");
        CertificateCreation storage cert = certificates[_id];
        require(cert.isActive, "Certificate is not active");
        require(_industry != mainIndustry, "Only Industry can delete Certificates");
        cert.isActive = false;
        delete expireCertificates[_id];
    }

    function isDeleteRequest(uint256 _id) public view returns (address){
        require(_id < nextCertificateId, "Certificate does not exist");
        return expireCertificates[_id];
    }

    // Function to check if an address is a nominee for a certificate
    function isNominee(uint256 _id, address _address) public view returns (bool) {
        require(_id < nextCertificateId, "Certificate does not exist");
        return certificates[_id].nominees[_address];
    }

    function hasRole(address _address) public view returns (string memory) {
        return roles[_address];
    }

    function updateRole(address _address, string memory role) public {
        roles[_address] = role;
    }

    function getTempCount() public view returns(uint256){
        return tempCount;
    }

    function setTempCount() public payable{
        tempCount = tempCount+1;
    }
}