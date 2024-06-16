# Report
> description

## Target
```
export TARGET=0.0.0.0
```

## Scans

```
nmap -A -p- -T4 $TARGET
```

## Findings

### FTP
```
ftp $TARGET
```

### SSH
```
ssh $TARGET
```

### SMB
```
smbclient -L \\\\$TARGET
smbclient \\\\$TARGET\\share
```

### WEB
#### sub domains
#### directories
#### XSS
#### upload


## Credentials / Keys
