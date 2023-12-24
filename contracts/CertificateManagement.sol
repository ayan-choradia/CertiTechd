// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CertificateManagement {
    struct CertificateCreation {
        uint256 id;
        address carrier;
        address recipient;  // Main owner
        mapping(address => bool) nominees;  // Updated to mapping
        mapping(uint256 => Change) changes; // Map change ID to Change struct
        uint256 changesCount; // Counter for tracking changes
        string data;
        bool isFinalized;
        mapping(address => bool) approvals;
        uint256[] collaboratorIds; // List of collaborator IDs for this certificate
        uint256 manufacturingDate;
        uint256 expiryDate;
    }

    struct Collaborator {
        bool hasViewAccess;
        bool hasOwnership;
    }

    struct Change {
        uint256 changeId;
        address initiator;
        string updatedData;
        mapping(address => bool) approvals;
        bool isApproved;
    }

    mapping(uint256 => CertificateCreation) public certificates;
    mapping(uint256 => mapping(address => Collaborator)) public collaborators;

    uint256 public nextCertificateId;

    // Function to create a new certificate
    function createCertificate(
        address _recipient,
        string memory _data,
        uint256 _manufacturingDate,
        uint256 _expiryDate
    ) public {
        uint256 newId = nextCertificateId;
        CertificateCreation storage newCertificate = certificates[newId];
        newCertificate.id = newId;
        newCertificate.carrier = msg.sender;
        newCertificate.recipient = _recipient;
        newCertificate.data = _data;
        newCertificate.isFinalized = false;
        newCertificate.collaboratorIds.push(newId); // Add the carrier as the first collaborator
        collaborators[newId][msg.sender].hasOwnership = true;
        newCertificate.manufacturingDate = _manufacturingDate;
        newCertificate.expiryDate = _expiryDate;
        nextCertificateId++;
    }

    // Function to request changes to a certificate
    function requestChanges(uint256 _id, string memory _updatedData) public {
        require(_id < nextCertificateId, "Certificate does not exist");
        CertificateCreation storage cert = certificates[_id];
        require(cert.carrier != msg.sender, "Only non-carriers can request changes");

      

        cert.changesCount++;

        // Once all parties sign off, update the certificate
        // For simplicity, let's assume all parties approved the changes
        cert.data = _updatedData;
        cert.isFinalized = true;
    }

    // Function to approve changes to a certificate
    function approveChanges(uint256 _id, uint256 _changeId) public {
        require(_id < nextCertificateId, "Certificate does not exist");
        CertificateCreation storage cert = certificates[_id];
        require(cert.carrier == msg.sender || collaborators[_id][msg.sender].hasOwnership, "Only the carrier or collaborator with ownership can approve changes");

        // Ensure the change ID is valid
        require(_changeId < cert.changesCount, "Invalid change ID");

        // Approve the change
        cert.changes[_changeId].approvals[msg.sender] = true;
        cert.changes[_changeId].isApproved = true;
    }

    // Function to transfer ownership to another address
    function transferOwnership(uint256 _id, address _newOwner) public {
        require(_id < nextCertificateId, "Certificate does not exist");
        CertificateCreation storage cert = certificates[_id];
        require(msg.sender == cert.carrier, "Only the current owner can transfer ownership");

        // Remove the current owner as the carrier and add the new owner
        cert.carrier = _newOwner;

        // Transfer ownership in collaborators mapping
        collaborators[_id][_newOwner] = collaborators[_id][msg.sender];
        delete collaborators[_id][msg.sender];
    }

    // Function to add a collaborator with view access
    function addCollaborator(uint256 _id, address _collaborator) public {
        require(_id < nextCertificateId, "Certificate does not exist");
        CertificateCreation storage cert = certificates[_id];
        require(msg.sender == cert.carrier || collaborators[_id][msg.sender].hasOwnership, "Only the carrier or collaborator with ownership can add collaborators");

        // Add the collaborator to the collaborator mapping with view access
        collaborators[_id][_collaborator].hasViewAccess = true;
        // Add the collaborator ID to the certificate's collaboratorIds array
        cert.collaboratorIds.push(_id);
    }

    // Function to remove a collaborator
    function removeCollaborator(uint256 _id, address _collaborator) public {
        require(_id < nextCertificateId, "Certificate does not exist");
        CertificateCreation storage cert = certificates[_id];
        require(msg.sender == cert.carrier || collaborators[_id][msg.sender].hasOwnership, "Only the carrier or collaborator with ownership can remove collaborators");

        // Remove the collaborator from the collaborator mapping
        delete collaborators[_id][_collaborator];
        // Remove the collaborator ID from the certificate's collaboratorIds array
        for (uint256 i = 0; i < cert.collaboratorIds.length; i++) {
            if (cert.collaboratorIds[i] == _id) {
                cert.collaboratorIds[i] = cert.collaboratorIds[cert.collaboratorIds.length - 1];
                cert.collaboratorIds.pop();
                break;
            }
        }
    }

   // Function to add a nominee
    function addNominee(uint256 _id, address _nominee) public {
        require(_id < nextCertificateId, "Certificate does not exist");
        CertificateCreation storage cert = certificates[_id];
        require(cert.recipient == msg.sender, "Only the main owner can add nominees");

        // Add the nominee to the nominees mapping
        cert.nominees[_nominee] = true;
    }

    // Function to remove a nominee
    function removeNominee(uint256 _id, address _nominee) public {
        require(_id < nextCertificateId, "Certificate does not exist");
        CertificateCreation storage cert = certificates[_id];
        require(cert.recipient == msg.sender, "Only the main owner can remove nominees");

        // Remove the nominee from the nominees mapping
        delete cert.nominees[_nominee];
    }

    // Function to retrieve certificate details
    function getCertificate(uint256 _id) public view returns (address, string memory, bool) {
        require(_id < nextCertificateId, "Certificate does not exist");
        CertificateCreation storage cert = certificates[_id];
        return (cert.carrier, cert.data, cert.isFinalized);
    }

    // Function to retrieve collaborator details
    function getCollaboratorDetails(uint256 _id, address _collaborator) public view returns (bool, bool) {
        require(_id < nextCertificateId, "Certificate does not exist");
        return (collaborators[_id][_collaborator].hasViewAccess, collaborators[_id][_collaborator].hasOwnership);
    }

  // Function to check if an address is a nominee for a certificate
function isNominee(uint256 _id, address _address) public view returns (bool) {
    require(_id < nextCertificateId, "Certificate does not exist");
    return certificates[_id].nominees[_address];
}
}