from direct.directnotify.DirectNotifyGlobal import *
from otp.ai.AIBaseGlobal import *
from toontown.building import DistributedBuildingAI
from toontown.building import GagshopBuildingAI
from toontown.building import HQBuildingAI
from toontown.building import KartShopBuildingAI
from toontown.building import PetshopBuildingAI
from toontown.hood import ZoneUtil
# from toontown.building import DistributedAnimBuildingAI


class DistributedBuildingMgrAI:
    notify = directNotify.newCategory('DistributedBuildingMgrAI')

    def __init__(self, air, branchId, dnaStore, trophyMgr):
        self.air = air
        self.branchId = branchId
        self.canonicalBranchId = ZoneUtil.getCanonicalZoneId(self.branchId)
        self.dnaStore = dnaStore
        self.trophyMgr = trophyMgr
        self.__buildings = {}
        self.findAllLandmarkBuildings()

    def cleanup(self):
        for building in self.__buildings.values():
            building.cleanup()
        self.__buildings = {}

    def isValidBlockNumber(self, blockNumber):
        return blockNumber in self.__buildings

    def isSuitBlock(self, blockNumber):
        if not self.isValidBlockNumber(blockNumber):
            return False
        return self.__buildings[blockNumber].isSuitBlock()

    def getSuitBlocks(self):
        blocks = []
        for blockNumber, building in self.__buildings.items():
            if building.isSuitBlock():
                blocks.append(blockNumber)
        return blocks

    def getEstablishedSuitBlocks(self):
        blocks = []
        for blockNumber, building in self.__buildings.items():
            if building.isEstablishedSuitBlock():
                blocks.append(blockNumber)
        return blocks

    def getToonBlocks(self):
        blocks = []
        for blockNumber, building in self.__buildings.items():
            if isinstance(building, HQBuildingAI.HQBuildingAI):
                continue
            if isinstance(building, KartShopBuildingAI.KartShopBuildingAI):
                continue
            if not building.isSuitBlock():
                blocks.append(blockNumber)
        return blocks

    def getBuildings(self):
        return self.__buildings.values()

    def getFrontDoorPoint(self, blockNumber):
        if self.isValidBlockNumber(blockNumber):
            return self.__buildings[blockNumber].getFrontDoorPoint()

    def getBuildingTrack(self, blockNumber):
        if self.isValidBlockNumber(blockNumber):
            return self.__buildings[blockNumber].track

    def getBuilding(self, blockNumber):
        if self.isValidBlockNumber(blockNumber):
            return self.__buildings[blockNumber]

    def setFrontDoorPoint(self, blockNumber, point):
        if self.isValidBlockNumber(blockNumber):
            return self.__buildings[blockNumber].setFrontDoorPoint(point)

    def getDNABlockLists(self):
        blocks = []
        hqBlocks = []
        gagshopBlocks = []
        petshopBlocks = []
        kartshopBlocks = []
        animBldgBlocks = []
        for i in xrange(self.dnaStore.getNumBlockNumbers()):
            blockNumber = self.dnaStore.getBlockNumberAt(i)
            buildingType = self.dnaStore.getBlockBuildingType(blockNumber)
            if buildingType == 'hq':
                hqBlocks.append(blockNumber)
            elif buildingType == 'gagshop':
                gagshopBlocks.append(blockNumber)
            elif buildingType == 'petshop':
                petshopBlocks.append(blockNumber)
            elif buildingType == 'kartshop':
                kartshopBlocks.append(blockNumber)
            elif buildingType == 'animbldg':
                animBldgBlocks.append(blockNumber)
            else:
                blocks.append(blockNumber)
        return (blocks, hqBlocks, gagshopBlocks, petshopBlocks, kartshopBlocks,
                animBldgBlocks)

    def findAllLandmarkBuildings(self):
        (blocks, hqBlocks, gagshopBlocks, petshopBlocks, kartshopBlocks,
         animBldgBlocks) = self.getDNABlockLists()
        for blockNumber in blocks:
            self.newBuilding(blockNumber)
        for blockNumber in animBldgBlocks:
            self.newAnimBuilding(blockNumber)
        for blockNumber in hqBlocks:
            self.newHQBuilding(blockNumber)
        for blockNumber in gagshopBlocks:
            self.newGagshopBuilding(blockNumber)
        for block in petshopBlocks:
            self.newPetshopBuilding(block)
        for block in kartshopBlocks:
            self.newKartShopBuilding(block)

    def newBuilding(self, blockNumber):
        building = DistributedBuildingAI.DistributedBuildingAI(
            self.air, blockNumber, self.branchId, self.trophyMgr)
        building.generateWithRequired(self.branchId)
        building.setState('toon')
        self.__buildings[blockNumber] = building
        return building

    def newAnimBuilding(self, blockNumber):
        return  # TODO

    def newHQBuilding(self, blockNumber):
        dnaStore = self.air.dnaStoreMap[self.canonicalBranchId]
        exteriorZoneId = dnaStore.getZoneFromBlockNumber(blockNumber)
        exteriorZoneId = ZoneUtil.getTrueZoneId(exteriorZoneId, self.branchId)
        interiorZoneId = (self.branchId - (self.branchId%100)) + 500 + blockNumber
        building = HQBuildingAI.HQBuildingAI(
            self.air, exteriorZoneId, interiorZoneId, blockNumber)
        self.__buildings[blockNumber] = building
        return building

    def newGagshopBuilding(self, blockNumber):
        dnaStore = self.air.dnaStoreMap[self.canonicalBranchId]
        exteriorZoneId = dnaStore.getZoneFromBlockNumber(blockNumber)
        exteriorZoneId = ZoneUtil.getTrueZoneId(exteriorZoneId, self.branchId)
        interiorZoneId = (self.branchId - (self.branchId%100)) + 500 + blockNumber
        building = GagshopBuildingAI.GagshopBuildingAI(
            self.air, exteriorZoneId, interiorZoneId, blockNumber)
        self.__buildings[blockNumber] = building
        return building

    def newPetshopBuilding(self, blockNumber):
        dnaStore = self.air.dnaStoreMap[self.canonicalBranchId]
        exteriorZoneId = dnaStore.getZoneFromBlockNumber(blockNumber)
        exteriorZoneId = ZoneUtil.getTrueZoneId(exteriorZoneId, self.branchId)
        interiorZoneId = (self.branchId - (self.branchId%100)) + 500 + blockNumber
        building = PetshopBuildingAI.PetshopBuildingAI(
            self.air, exteriorZoneId, interiorZoneId, blockNumber)
        self.__buildings[blockNumber] = building
        return building

    def newKartShopBuilding(self, blockNumber):
        dnaStore = self.air.dnaStoreMap[self.canonicalBranchId]
        exteriorZoneId = dnaStore.getZoneFromBlockNumber(blockNumber)
        exteriorZoneId = ZoneUtil.getTrueZoneId(exteriorZoneId, self.branchId)
        interiorZoneId = (self.branchId - (self.branchId%100)) + 500 + blockNumber
        building = KartShopBuildingAI.KartShopBuildingAI(
            self.air, exteriorZoneId, interiorZoneId, blockNumber)
        self.__buildings[blockNumber] = building
        return building
