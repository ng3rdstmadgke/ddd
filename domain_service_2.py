
class PhysicalDistributionBase:
    """物流拠点を表すエンティティ"""
    def __init__(self):
        self.baggages = set()

    def ship(self, baggage):
        self.baggages.remove(baggage)

    def receive(self, baggage):
        self.baggages.add(baggage)


class TransportService:
    """輸送の振る舞いを定義するドメインサービス"""
    def transport(self, src: PhysicalDistributionBase, dst: PhysicalDistributionBase, baggage):
        src.ship(baggage)
        dst.receive(baggage)

if __name__ == "__main__":

    # 物流拠点を用意
    base1 = PhysicalDistributionBase()
    base2 = PhysicalDistributionBase()

    # 荷物を base1 に登録
    baggage = "b1"
    base1.receive(baggage)

    # base1 -> base2 に baggage を輸送
    transport_service = TransportService()
    transport_service.transport(base1, base2, baggage)
