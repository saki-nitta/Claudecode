/**
 * おもちゃのバトン 古物台帳 GAS スクリプト
 * おもちゃと遊び企画舎 とうめいしっぽ（古物商許可取得済み）
 *
 * 使い方:
 *   1. Googleスプレッドシートを新規作成
 *   2. 拡張機能 → Apps Script → このコードを貼り付けて保存
 *   3. スプレッドシートに戻り「とうめいしっぽ台帳」メニュー → 「初回セットアップ」を実行
 */

const SHEET = {
  PURCHASE: '仕入れ台帳',
  BATON:    'バトン市記録',
  SALES:    '販売記録',
};

const HEADERS = {
  PURCHASE: [
    '管理番号', '取引日', '品名', 'ブランド', '品目区分',
    '特徴（色・サイズ・状態等）', '数量', '仕入れ価格（円）',
    '仕入れ先区分', '相手の氏名（1万円以上）', '相手の住所',
    '本人確認書類の種類', '本人確認書類の番号',
    '仕入れ先（プラットフォーム等）', '出品URL・取引ID',
    '販売予定価格（円）', '備考',
  ],
  BATON: [
    'イベント日', '参加者番号', '持ち込み品名', '持ち込み品の特徴',
    '発行TOY枚数', '受け取り品名', '受け取り品の特徴',
    '追加TOY購入枚数', '追加TOY購入金額（円）', '決済方法', '備考',
  ],
  SALES: [
    '管理番号', '品名', '販売日', '販売先',
    '販売価格（円）', '手数料（円）', '実売上（円）',
    '仕入れ価格（円）', '利益（円）', '備考',
  ],
};

const HEADER_COLOR = '#4a7c59';
const HEADER_FONT  = '#ffffff';

// ─── メニュー ──────────────────────────────────────────

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('とうめいしっぽ台帳')
    .addItem('① 初回セットアップ（シート作成）', 'setupSheets')
    .addItem('② 初期データ投入（T001〜T003）', 'insertInitialData')
    .addSeparator()
    .addItem('次の管理番号を確認', 'showNextId')
    .addItem('入力済み行を保護する', 'protectCompletedRows')
    .addSeparator()
    .addItem('月次バックアップを実行', 'monthlyBackup')
    .addToUi();
}

// ─── 初期データ投入（T001〜T003） ────────────────────────────

function insertInitialData() {
  const ss    = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(SHEET.PURCHASE);
  if (!sheet) {
    SpreadsheetApp.getUi().alert('先に「初回セットアップ」を実行してください。');
    return;
  }

  // 既にデータがある場合は確認する
  if (sheet.getLastRow() > 1) {
    const ui  = SpreadsheetApp.getUi();
    const res = ui.alert('既にデータがあります。追加してもいいですか？', ui.ButtonSet.YES_NO);
    if (res !== ui.Button.YES) return;
  }

  // 列順: 管理番号,取引日,品名,ブランド,品目区分,特徴,数量,仕入れ価格,
  //       仕入れ先区分,相手氏名,相手住所,本人確認種類,本人確認番号,
  //       仕入れ先(PF),出品URL・取引ID,販売予定価格,備考
  const rows = [
    [
      'T001', '2026/5/8',
      'KAPLA 木製積み木セット 収納ボックス付き', 'KAPLA（カプラ）', 'おもちゃ（木製積み木）',
      '木製・188ピース（本来200ピース・印字品1点欠品）・収納ボックス付き（ボックスにはがれあり）・多少使用感あり',
      1, 3800, '個人', '', '', '', '',
      'メルカリ', 'm89159370528', '', '',
    ],
    [
      'T002', '2026/5/8',
      '木製知育玩具5点セット（ラトル・スターコマ他）',
      'HEIMESS / Milky Toy / エド・インター / ナカムラ工房', 'おもちゃ（木製知育玩具）',
      '①スターコマ ハイメス ②どうぶつラトル かたつむり ③ボンボンラトル ④エッグトーストのラトル ⑤はじめてのつみき／ユーズド品・細かなダメージ・剥げあり',
      '5点セット', 1100, '個人', '', '', '', '',
      'メルカリ', 'm98122724970', '', '',
    ],
    [
      'T003', '2026/5/8',
      'nic ポストボックス＆PLUS10', 'nic（ニック社）', 'おもちゃ（木製）',
      'ポストボックス（車付き・引っ張り紐はダイソー品に付け替え）＋PLUS10（ボロボロ・箱あり・サイコロ紐等パーツなし）',
      '2点（セット）', 4200, '個人', '', '', '', '',
      'メルカリ', 'm15557208625', '',
      'PLUS10は保管中（セット完成待ち）。ポストボックスは単品販売またはバトン市向け。',
    ],
  ];

  const startRow = sheet.getLastRow() + 1;
  sheet.getRange(startRow, 1, rows.length, rows[0].length).setValues(rows);

  SpreadsheetApp.getUi().alert(
    '✅ 初期データ投入完了！\nT001〜T003を仕入れ台帳に追加しました。\n\n入力後は「入力済み行を保護する」を実行してください。'
  );
}

// ─── 初回セットアップ ────────────────────────────────────

function setupSheets() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();

  _createSheet(ss, SHEET.PURCHASE, HEADERS.PURCHASE);
  _createSheet(ss, SHEET.BATON,    HEADERS.BATON);
  _createSheet(ss, SHEET.SALES,    HEADERS.SALES);

  // デフォルトの「シート1」を削除（空のまま残っている場合）
  const defaultSheet = ss.getSheetByName('シート1');
  if (defaultSheet && ss.getNumSheets() > 3) {
    ss.deleteSheet(defaultSheet);
  }

  SpreadsheetApp.getUi().alert(
    '✅ セットアップ完了！\n\n' +
    '3つのシートを作成しました。\n\n' +
    '【次にやること】\n' +
    '・ファイル → 変更履歴 → 「変更履歴を表示」で履歴機能を確認\n' +
    '・データを入力したら「入力済み行を保護する」を実行してください'
  );
}

function _createSheet(ss, name, headers) {
  let sheet = ss.getSheetByName(name);
  if (!sheet) {
    sheet = ss.insertSheet(name);
  }

  // ヘッダー行を設定
  const headerRange = sheet.getRange(1, 1, 1, headers.length);
  headerRange.setValues([headers]);
  headerRange.setBackground(HEADER_COLOR);
  headerRange.setFontColor(HEADER_FONT);
  headerRange.setFontWeight('bold');
  headerRange.setWrap(true);
  sheet.setFrozenRows(1);

  // 列幅を調整
  sheet.setColumnWidths(1, headers.length, 130);

  return sheet;
}

// ─── 管理番号の採番 ──────────────────────────────────────

function getNextPurchaseId() {
  const ss    = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(SHEET.PURCHASE);
  if (!sheet || sheet.getLastRow() <= 1) return 'T001';

  const ids = sheet
    .getRange(2, 1, sheet.getLastRow() - 1, 1)
    .getValues()
    .flat()
    .filter(v => /^T\d+$/.test(String(v)));

  if (ids.length === 0) return 'T001';

  const maxNum = Math.max(...ids.map(id => parseInt(id.slice(1), 10)));
  return 'T' + String(maxNum + 1).padStart(3, '0');
}

function showNextId() {
  SpreadsheetApp.getUi().alert('次の管理番号: ' + getNextPurchaseId());
}

// ─── 入力済み行の保護 ────────────────────────────────────

function protectCompletedRows() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const me = Session.getEffectiveUser();

  [SHEET.PURCHASE, SHEET.BATON, SHEET.SALES].forEach(name => {
    const sheet = ss.getSheetByName(name);
    if (!sheet) return;

    const lastRow = sheet.getLastRow();
    if (lastRow <= 1) return;

    // 既存の範囲保護を全削除してから再設定（重複防止）
    sheet.getProtections(SpreadsheetApp.ProtectionType.RANGE)
      .forEach(p => p.remove());

    // ヘッダー行を保護
    _protect(sheet.getRange(1, 1, 1, sheet.getLastColumn()), 'ヘッダー行', me);

    // データ行を保護
    _protect(sheet.getRange(2, 1, lastRow - 1, sheet.getLastColumn()), '記入済みデータ（改ざん防止）', me);
  });

  SpreadsheetApp.getUi().alert(
    '✅ 保護完了！\n' +
    '入力済みのデータを読み取り専用に設定しました。\n' +
    '（自分のアカウントからは引き続き編集できます）'
  );
}

function _protect(range, description, me) {
  const protection = range.protect().setDescription(description);
  // 自分以外の編集を禁止
  protection.addEditor(me);
  const others = protection.getEditors().filter(e => e.getEmail() !== me.getEmail());
  if (others.length > 0) protection.removeEditors(others);
  if (protection.canDomainEdit()) protection.setDomainEdit(false);
}

// ─── 販売記録の自動入力（onEdit トリガー） ──────────────────

/**
 * 販売記録シートのA列（管理番号）を入力すると
 * 仕入れ台帳から品名・仕入れ価格を自動補完する
 */
function onEdit(e) {
  const sheet = e.range.getSheet();
  if (sheet.getName() !== SHEET.SALES) return;

  const row = e.range.getRow();
  if (row <= 1) return;

  const col = e.range.getColumn();

  // A列（管理番号）入力 → 品名・仕入れ価格を自動補完
  if (col === 1) {
    _fillFromPurchaseLedger(sheet, row, e.range.getValue());
    return;
  }

  // E列（販売価格）またはF列（手数料）変更 → G列・I列を再計算
  if (col === 5 || col === 6) {
    _recalcProfit(sheet, row);
  }
}

function _fillFromPurchaseLedger(salesSheet, row, managementId) {
  if (!managementId) return;

  const ss            = SpreadsheetApp.getActiveSpreadsheet();
  const purchaseSheet = ss.getSheetByName(SHEET.PURCHASE);
  if (!purchaseSheet) return;

  const data  = purchaseSheet.getDataRange().getValues();
  const found = data.find(r => String(r[0]) === String(managementId));
  if (!found) return;

  // B列: 品名（仕入れ台帳のC列 = index 2）
  salesSheet.getRange(row, 2).setValue(found[2]);
  // H列: 仕入れ価格（仕入れ台帳のH列 = index 7）
  salesSheet.getRange(row, 8).setValue(found[7]);
}

function _recalcProfit(sheet, row) {
  const salesPrice   = Number(sheet.getRange(row, 5).getValue()) || 0;
  const fee          = Number(sheet.getRange(row, 6).getValue()) || 0;
  const purchasePrice = Number(sheet.getRange(row, 8).getValue()) || 0;

  const realSales = salesPrice - fee;
  const profit    = realSales - purchasePrice;

  sheet.getRange(row, 7).setValue(realSales); // G列: 実売上
  sheet.getRange(row, 9).setValue(profit);    // I列: 利益
}

// ─── 月次バックアップ ────────────────────────────────────

function monthlyBackup() {
  const ss      = SpreadsheetApp.getActiveSpreadsheet();
  const now     = new Date();
  const dateStr = Utilities.formatDate(now, 'Asia/Tokyo', 'yyyyMM');
  const name    = `とうめいしっぽ_古物台帳_バックアップ_${dateStr}`;

  // 同名バックアップが既にある場合はスキップ
  const existing = DriveApp.getFilesByName(name);
  if (existing.hasNext()) {
    SpreadsheetApp.getUi().alert(`今月のバックアップは既にあります:\n${name}`);
    return;
  }

  ss.copy(name);
  SpreadsheetApp.getUi().alert(
    `✅ バックアップ完了！\n\nファイル名: ${name}\nGoogleドライブ（マイドライブ）に保存しました。`
  );
}