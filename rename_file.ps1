$dir = 'G:\番剧\物语系列\Season 0'

Set-Location $dir

# 初始化计数器
$counter = 42

# 获取文件并处理（添加排序保证顺序）
Get-ChildItem -Path $dir -Filter '续*.mkv' | Sort-Object Name | ForEach-Object {
    # 分离文件名和扩展名
    $newName = "$($_.BaseName) S00E$($counter.ToString('00'))$($_.Extension)"

    # 执行重命名
    Move-Item -LiteralPath $_.FullName -Destination $newName

    # 计数器递增
    $counter++
}
