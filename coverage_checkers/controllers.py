from coverage_checkers.providers.lowi import LowiChecker


class CheckerCoverageController:
    @staticmethod
    def check_address(address):
        return LowiChecker(address).has_coverage()
