"""
おもちゃのバトン市 利益シミュレーター
1TOY = 1円・会場内限定通貨
"""

def simulate(
    participants=10,          # 参加者数（人）
    participation_fee=500,    # 参加費（円/人）
    items_per_person=3,       # 1人あたり平均持ち込み点数
    tier_s=0.2,               # Sティア比率（HABA等の上質ブランド）
    tier_a=0.4,               # Aティア比率（くもん等の中堅ブランド）
    tier_b=0.4,               # Bティア比率（一般ブランド）
    cash_buyer_ratio=0.7,     # TOY追加購入する参加者の割合（制限なし）
    cash_avg_yen=500,         # TOY追加購入の1人あたり平均金額（円）
    saki_items=5,             # 新田さん仕入れ品の出品数（点）
    saki_cost_per_item=800,   # 仕入れ品の平均原価（メルカリ購入金額）
    saki_markup=1.2,          # 売値 = 仕入れ値 × この倍率（基本1.2）
    unused_ratio=0.1,         # 未使用TOYの割合（失効分）
):
    # ティア別TOY付与額（レンジの中央値・クロ更新案 2026/5/8）
    TOY_S = 400  # Sティア平均（300〜500の中央）
    TOY_A = 250  # Aティア平均（200〜300の中央）
    TOY_B = 150  # Bティア平均（100〜200の中央）

    # 持ち込みから発生するTOY
    total_items = participants * items_per_person
    toy_from_items = (
        int(total_items * tier_s) * TOY_S +
        int(total_items * tier_a) * TOY_A +
        int(total_items * tier_b) * TOY_B
    )

    # 現金TOY購入
    cash_buyers = int(participants * cash_buyer_ratio)
    cash_revenue = cash_buyers * cash_avg_yen
    toy_from_cash = cash_revenue  # 1TOY=1円なので同額

    # TOY合計流通量
    total_toy = toy_from_items + toy_from_cash

    # 未使用TOY（失効分）のうち現金で買われたTOYの割合
    unused_total = total_toy * unused_ratio
    if total_toy > 0:
        unused_cash = unused_total * (toy_from_cash / total_toy)
    else:
        unused_cash = 0

    # 仕入れ品のTOY価格（仕入れ値 × マークアップ倍率）
    saki_toy_price = int(saki_cost_per_item * saki_markup)

    # 仕入れコスト
    saki_total_cost = saki_items * saki_cost_per_item

    # 参加費
    fee_revenue = participants * participation_fee

    # 収益
    total_revenue = fee_revenue + cash_revenue + unused_cash
    gross_profit = total_revenue - saki_total_cost

    # 損益分岐点（現金TOY購入による収益 ≥ 仕入れコスト）
    revenue_per_person = cash_buyer_ratio * cash_avg_yen
    if revenue_per_person > 0:
        breakeven = saki_total_cost / revenue_per_person
    else:
        breakeven = float('inf')

    # 出力
    print("=" * 52)
    print("  おもちゃのバトン市 利益シミュレーター")
    print("=" * 52)

    print("\n[入力条件]")
    print(f"  参加者数          : {participants}名")
    print(f"  参加費            : ¥{participation_fee}/人")
    print(f"  持ち込み          : 1人 {items_per_person}点平均")
    print(f"  ティア比率        : S {tier_s*100:.0f}% / A {tier_a*100:.0f}% / B {tier_b*100:.0f}%")
    print(f"  TOY追加購入       : {cash_buyer_ratio*100:.0f}%の参加者が平均¥{cash_avg_yen}（上限なし）")
    print(f"  仕入れ品出品数    : {saki_items}点（平均{saki_toy_price}TOY・原価¥{saki_cost_per_item}）")
    print(f"  未使用TOY率       : {unused_ratio*100:.0f}%")

    print("\n[TOY流通量]")
    print(f"  持ち込みから発生  : {toy_from_items:,} TOY")
    print(f"  現金購入分        : {toy_from_cash:,} TOY  （¥{cash_revenue:,}）")
    print(f"  合計              : {total_toy:,} TOY")
    print(f"  未使用（失効）    : 約{int(unused_total):,} TOY")

    print("\n[収支]")
    print(f"  参加費            : ¥{fee_revenue:,}  ({participants}名 × ¥{participation_fee})")
    print(f"  TOY追加購入売上   : ¥{cash_revenue:,}")
    print(f"  未使用TOY（現金分）: ¥{int(unused_cash):,}")
    print(f"  ─────────────────────")
    print(f"  収入合計          : ¥{int(total_revenue):,}")
    print(f"  仕入れコスト      : ¥{saki_total_cost:,}")
    print(f"  ─────────────────────")
    print(f"  粗 利             : ¥{int(gross_profit):,}")

    print("\n[損益分岐点]")
    if breakeven == float('inf'):
        print("  現金TOY購入がないため計算できません")
    else:
        print(f"  最低必要参加者数  : 約{int(breakeven)+1}名")

    print("=" * 52)

    return {
        "収入合計": int(total_revenue),
        "仕入れコスト": saki_total_cost,
        "粗利": int(gross_profit),
        "損益分岐点": int(breakeven)+1 if breakeven != float('inf') else None
    }


if __name__ == "__main__":
    print("\n【パターン①】控えめ（10名・TOY追加購入¥300・仕入れ5点）")
    simulate(
        participants=10, participation_fee=500,
        cash_avg_yen=300, cash_buyer_ratio=0.5,
        saki_items=5, saki_cost_per_item=800, saki_markup=1.2,
    )

    print("\n【パターン②】標準（10名・TOY追加購入¥500・仕入れ5点）")
    simulate(
        participants=10, participation_fee=500,
        cash_avg_yen=500, cash_buyer_ratio=0.7,
        saki_items=5, saki_cost_per_item=800, saki_markup=1.2,
    )

    print("\n【パターン③】TOY追加購入が多い場合（10名・¥1,000・仕入れ5点）")
    simulate(
        participants=10, participation_fee=500,
        cash_avg_yen=1000, cash_buyer_ratio=0.8,
        saki_items=5, saki_cost_per_item=800, saki_markup=1.2,
    )