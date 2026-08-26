// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AccessRecord {
    struct AccessLog {
        bytes32 userHash;
        bytes32 fileHash;
        uint256 timestamp;
        bool granted;
        string accessType; // "LOGIN", "FILE_ACCESS", "FILE_TAMPER"
    }

    mapping(uint256 => AccessLog) public accessRecords;
    mapping(bytes32 => uint256[]) public userAccessHistory;
    mapping(bytes32 => uint256[]) public fileAccessHistory;
    
    uint256 public recordCount;
    address public admin;

    event AccessRecorded(
        uint256 indexed recordId,
        bytes32 indexed userHash,
        bytes32 indexed fileHash,
        uint256 timestamp,
        bool granted,
        string accessType
    );

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can call this function");
        _;
    }

    constructor() {
        admin = msg.sender;
        recordCount = 0;
    }

    function recordAccess(
        bytes32 _userHash,
        bytes32 _fileHash,
        bool _granted,
        string memory _accessType
    ) public returns (uint256) {
        recordCount++;
        accessRecords[recordCount] = AccessLog({
            userHash: _userHash,
            fileHash: _fileHash,
            timestamp: block.timestamp,
            granted: _granted,
            accessType: _accessType
        });

        userAccessHistory[_userHash].push(recordCount);
        if (_fileHash != bytes32(0)) {
            fileAccessHistory[_fileHash].push(recordCount);
        }

        emit AccessRecorded(
            recordCount,
            _userHash,
            _fileHash,
            block.timestamp,
            _granted,
            _accessType
        );

        return recordCount;
    }

    function getAccessRecord(uint256 _recordId) public view returns (
        bytes32 userHash,
        bytes32 fileHash,
        uint256 timestamp,
        bool granted,
        string memory accessType
    ) {
        require(_recordId > 0 && _recordId <= recordCount, "Invalid record ID");
        AccessLog memory record = accessRecords[_recordId];
        return (
            record.userHash,
            record.fileHash,
            record.timestamp,
            record.granted,
            record.accessType
        );
    }

    function getUserAccessHistory(bytes32 _userHash) public view returns (uint256[] memory) {
        return userAccessHistory[_userHash];
    }

    function getFileAccessHistory(bytes32 _fileHash) public view returns (uint256[] memory) {
        return fileAccessHistory[_fileHash];
    }

    function getLatestFileHash(bytes32 _userHash) public view returns (bytes32) {
        uint256[] memory history = userAccessHistory[_userHash];
        if (history.length == 0) return bytes32(0);
        
        for (uint256 i = history.length; i > 0; i--) {
            uint256 recordId = history[i - 1];
            if (accessRecords[recordId].granted && 
                keccak256(abi.encodePacked(accessRecords[recordId].accessType)) == keccak256(abi.encodePacked("FILE_ACCESS"))) {
                return accessRecords[recordId].fileHash;
            }
        }
        return bytes32(0);
    }

    function verifyFileIntegrity(bytes32 _userHash, bytes32 _currentFileHash) public view returns (bool) {
        bytes32 storedHash = getLatestFileHash(_userHash);
        return storedHash == _currentFileHash && storedHash != bytes32(0);
    }

    function updateAdmin(address _newAdmin) public onlyAdmin {
        admin = _newAdmin;
    }

    function getTotalRecords() public view returns (uint256) {
        return recordCount;
    }
}