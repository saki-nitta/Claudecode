/**
 * 工作教室 材料費管理ツール セットアップスクリプト
 *
 * 【使い方】
 * 1. https://script.google.com にアクセスして「新しいプロジェクト」を作成
 * 2. このスクリプト全体をコピーして貼り付け（既存のコードは削除する）
 * 3. 上部メニューの「実行」→「setup工作教室材料費管理」を選択
 * 4. 権限の許可を求めるダイアログが出たら「許可」を押す
 * 5. 完了後、実行ログに表示されたURLからスプレッドシートとフォームを開く
 *
 * 【作成されるもの】
 * - Googleフォーム「工作教室 材料費記録フォーム」
 * - スプレッドシート「工作教室_材料費管理_R8」（フォームの回答・予算管理・集計ダッシュボードの3シート）
 *
 * 【センター別既知の予算額（R8）】
 * 高松:25,000円、青山:16,000円、北松園:16,000円、緑ヶ丘:15,000円、上米内:5,000円
 * ※ 加賀野・土淵・北厨川は不明のため空欄。入力後に予算残高が自動更新されます。
 */

function setup工作教室材料費管理() {

  // ──────────────────────────────────────
  // 1. スプレッドシートを作成
  // ──────────────────────────────────────
  const ss = SpreadsheetApp.create('工作教室_材料費管理_R8');
  const ssId = ss.getId();
  const ssUrl = ss.getUrl();

  // デフォルトで作られる「シート1」を「予算管理」に改名（後で使う）
  const defaultSheet = ss.getSheets()[0];
  defaultSheet.setName('予算管理');

  // ──────────────────────────────────────
  // 2. Googleフォームを作成してスプレッドシートにリンク
  // ──────────────────────────────────────
  const form = FormApp.create('工作教室 材料費記録フォーム');
  form.setDescription('工作教室の材料費を記録するフォームです。購入のたびに入力してください。');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ssId);

  // ── 購入日（日付）
  form.addDateItem()
    .setTitle('購入日')
    .setRequired(true);

  // ── 購入先（ラジオボタン＋その他に自由記述）
  // ※ Googleフォームの「プルダウン」はその他オプション非対応のため
  //    「ラジオボタン＋その他」形式で実装しています
  const shopItem = form.addMultipleChoiceItem();
  shopItem.setTitle('購入先')
    .setRequired(true)
    .setChoices([
      shopItem.createChoice('ダイソー'),
      shopItem.createChoice('セリア'),
      shopItem.createChoice('橋市'),
    ])
    .showOtherOption(true); // 「その他」選択時に自由記述欄が出る

  // ── 金額（数値）
  const amountItem = form.addTextItem();
  amountItem.setTitle('金額（円）')
    .setRequired(true);
  amountItem.setValidation(
    FormApp.createTextValidation()
      .requireNumberGreaterThanOrEqualTo(1)
      .build()
  );

  // ── センター名（プルダウン）
  const centerItem = form.addListItem();
  centerItem.setTitle('センター名')
    .setRequired(true)
    .setChoices([
      centerItem.createChoice('青山'),
      centerItem.createChoice('高松'),
      centerItem.createChoice('緑ヶ丘'),
      centerItem.createChoice('北松園'),
      centerItem.createChoice('上米内'),
      centerItem.createChoice('加賀野'),
      centerItem.createChoice('土淵'),
      centerItem.createChoice('北厨川'),
    ]);

  // ── メモ（任意）
  form.addParagraphTextItem()
    .setTitle('メモ（任意）')
    .setRequired(false);

  // ──────────────────────────────────────
  // 3. スプレッドシートのシートを整備
  // ──────────────────────────────────────
  // フォームのリンク後、「フォームの回答 1」シートが自動生成される
  SpreadsheetApp.flush(); // 反映を待つ

  // センター一覧（フォームと同じ順序）
  const centers = ['青山', '高松', '緑ヶ丘', '北松園', '上米内', '加賀野', '土淵', '北厨川'];

  // 既知の予算額（R8年度）。不明は 0 のまま空欄表示にする
  const budgetMap = {
    '高松':  25000,
    '青山':  16000,
    '北松園': 16000,
    '緑ヶ丘': 15000,
    '上米内':  5000,
    '加賀野':     0,
    '土淵':       0,
    '北厨川':     0,
  };

  // ── 3-A. 予算管理シートを構築 ────────────────
  const budgetSheet = ss.getSheetByName('予算管理') || ss.insertSheet('予算管理');

  // ヘッダー
  budgetSheet.getRange('A1:C1').setValues([['センター名', '予算額（円）', '備考']]);
  budgetSheet.getRange('A1:C1')
    .setBackground('#4a86e8')
    .setFontColor('#ffffff')
    .setFontWeight('bold');

  // データ行
  centers.forEach((center, i) => {
    const row = i + 2;
    const budget = budgetMap[center] || '';
    const note = (center === '青山' || center === '高松')
      ? '毎月レシート提出あり'
      : '';
    budgetSheet.getRange(row, 1).setValue(center);
    budgetSheet.getRange(row, 2).setValue(budget);
    budgetSheet.getRange(row, 3).setValue(note);
  });

  // 列幅調整
  budgetSheet.setColumnWidth(1, 120);
  budgetSheet.setColumnWidth(2, 130);
  budgetSheet.setColumnWidth(3, 200);

  // 予算額列に数値書式
  budgetSheet.getRange('B2:B9').setNumberFormat('#,##0');

  // 予算管理シートのA・C列を保護（センター名と備考は変更させない）
  const budgetProtect = budgetSheet.getRange('A2:A9').protect();
  budgetProtect.setDescription('センター名は変更しないでください');
  budgetProtect.setWarningOnly(true); // 警告のみ（編集は可能だが確認が出る）

  // ── 3-B. 集計ダッシュボードシートを構築 ────────────────
  // ※ フォームの回答シートの列構成（GASでフォームを作成した場合）：
  //   A: タイムスタンプ
  //   B: 購入日
  //   C: 購入先
  //   D: 金額（円）
  //   E: センター名
  //   F: メモ（任意）

  const dashSheet = ss.insertSheet('集計ダッシュボード');

  // タイトル
  dashSheet.getRange('A1').setValue('工作教室 材料費 集計ダッシュボード（R8年度）');
  dashSheet.getRange('A1').setFontSize(14).setFontWeight('bold');

  // 更新案内
  dashSheet.getRange('A2').setValue('※ フォームに入力があると自動で更新されます');
  dashSheet.getRange('A2').setFontColor('#666666').setFontStyle('italic');

  // ヘッダー行（4行目）
  const dashHeaders = ['センター名', '予算額（円）', '使用総額（円）', '予算残高（円）'];
  dashSheet.getRange('A4:D4').setValues([dashHeaders]);
  dashSheet.getRange('A4:D4')
    .setBackground('#4a86e8')
    .setFontColor('#ffffff')
    .setFontWeight('bold');

  // データ行（5行目以降）
  centers.forEach((center, i) => {
    const row = i + 5;
    const budgetRef = `予算管理!B${i + 2}`;

    // センター名
    dashSheet.getRange(row, 1).setValue(center);

    // 予算額（予算管理シートから参照）
    dashSheet.getRange(row, 2).setFormula(`=${budgetRef}`);

    // 使用総額（フォームの回答からSUMIF）
    // 'フォームの回答 1'!E列がセンター名、D列が金額
    dashSheet.getRange(row, 3).setFormula(
      `=IFERROR(SUMIF('フォームの回答 1'!E:E,A${row},'フォームの回答 1'!D:D),0)`
    );

    // 予算残高（予算額 - 使用総額）
    dashSheet.getRange(row, 4).setFormula(`=B${row}-C${row}`);
  });

  // 数値書式
  dashSheet.getRange('B5:D12').setNumberFormat('#,##0');

  // 残高がマイナスの場合に赤表示（条件付き書式）
  const redRule = SpreadsheetApp.newConditionalFormatRule()
    .whenNumberLessThan(0)
    .setFontColor('#cc0000')
    .setBackground('#ffe0e0')
    .setRanges([dashSheet.getRange('D5:D12')])
    .build();
  dashSheet.setConditionalFormatRules([redRule]);

  // 列幅調整
  dashSheet.setColumnWidth(1, 120);
  dashSheet.setColumnWidth(2, 130);
  dashSheet.setColumnWidth(3, 130);
  dashSheet.setColumnWidth(4, 130);

  // ダッシュボードの数式セルを保護（誤操作防止）
  const dashProtect = dashSheet.getRange('B5:D12').protect();
  dashProtect.setDescription('自動集計セルのため変更しないでください');
  dashProtect.setWarningOnly(true);

  // ── 3-C. シートの順番を整える（左から：フォームの回答1 → 予算管理 → 集計ダッシュボード）
  const allSheets = ss.getSheets();
  const formResponseSheet = allSheets.find(s => s.getName().startsWith('フォームの回答'));
  if (formResponseSheet) {
    ss.setActiveSheet(formResponseSheet);
    ss.moveActiveSheet(1);
  }
  ss.setActiveSheet(budgetSheet);
  ss.moveActiveSheet(2);
  ss.setActiveSheet(dashSheet);
  ss.moveActiveSheet(3);

  // ──────────────────────────────────────
  // 4. 完了メッセージ
  // ──────────────────────────────────────
  const formUrl = form.getPublishedUrl();
  const formEditUrl = form.getEditUrl();

  console.log('✅ セットアップ完了！');
  console.log('');
  console.log('📊 スプレッドシート: ' + ssUrl);
  console.log('📝 フォーム（回答用）: ' + formUrl);
  console.log('🔧 フォーム（編集用）: ' + formEditUrl);
  console.log('');
  console.log('【次のステップ】');
  console.log('1. スプレッドシートを開いて「予算管理」シートで加賀野・土淵・北厨川の予算額を入力する');
  console.log('2. フォーム（回答用）URLを各センター担当者と共有する');
  console.log('3. 「集計ダッシュボード」で予算残高を確認する');
}
