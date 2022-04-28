# car_optim
マツダベンチマークを用いた単目的最適化(Platypusライブラリ使用)


## タスク説明
車体構造開発のために重み最小化の単一目的最適化または重量の最小化と一般的な厚さの部品の最大化の多目的最適化問題を扱う。設計変数は各構造部品の板厚で222個(74部品×3車種)。制約条件は衝突安全性能等合計54個。

[応答曲面法を用いた複数車種の同時最適化ベンチマーク問題](https://ladse.eng.isas.jaxa.jp/benchmark/jpn/index.html)


## 環境構築
```bash
conda env create -n car_optim -f car_optim.yml
```

## 実行
```bash
python main.py
```

## 結果
総重量の最小化を目的とした最適化の結果

| アルゴリズム   |  実行時間[s]   |  目的関数値  　|
|---            | ----          | ----          |
|NSGA-II        |  4.24         |  2.20         |
|SMPSO          |  2.68         |  2.78         |



## データセット説明
以降はデータセット内に含まれるreadme.txtを和訳・要約したもの。
ただし、Windows部分のみを扱っています。

#### 概要
設計変数データセット(pop_vars_eval.txt)を入力として読み込み、
目的関数データセット(pop_objs_eval.txt)を制約関数データセット
(pop_cons_eval.txt)を出力。

実行する際はbinディレクトリ内の64bit　Windows用のバイナリファイルを使用可能。
もし動作しない場合は、プログラムをコンパイルした後にバイナリファイルを作成。

#### コンパイル方法
※Visual Studio 2015、2017で検証済

- 2台最適化の場合
1. ./src/vs2015/mazda_mop.sln
2. Build
すると mozada_mop_sca.exeがReleaseディレクトリに作成

- 3台最適化の場合
1. ./src/vs2015/mazda_sca.sln
2. Build
すると mozada_mop_sca.exeがReleaseディレクトリに作成

#### 入出力ファイルフォーマット
- 設計変数データセット(pop_vars_eval.txt) <br>
各行が個体、各列が各設計変数に対応。列はタブで区切る。
このベンチマーク問題は222個の変数があるため、1行に222個のタブで
区切られた数値文字列を作成する必要。行数は1以上にしてください。

- 目的関数データセット(pop_objs_eval.txt) <br>
各行は独立、設計変数データセット(pop_vars_eval.txt)の各行の結果に対応。
タブで区切られた各列は、目的関数と補足情報。 
    - 1列目：3台の車両の総重量
    - 2列目：共通ゲージパーツの数
    - 3列目：SUVの重量
    - 4列目：LVの重量
    - 5列目：SVの重量

- 制約関数データセット(pop_cons_eval.txt) <br>
各行は独立、設計変数データセット(pop_vars_eval.txt)の各行の結果に対応。
タブで区切られた各列は制約関数の値。
各列の意味は、Excelの "Info_Mazda_CdMOBP.xlsx "を参照。

#### 実行方法
コンパイルしたプログラムを実行する場合、入力ファイルがあるパスを指定。 
実行例として、Windows 用の run.batがサンプルディレクトリにあります。

``` bash
mazda_mop.exe the-path-to-the-input-file
```
