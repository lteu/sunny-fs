<?

/**
*
*
* A html based visualiser for sunny performance on feature selected dataset
*
*
*/

$fss = array("original","ranker3","ranker5","ranker7","ranker9","ranker11","ranker13","ranker15","ranker17");
$instFilePath = "inst.txt";

$content = "";
$scenarios = array();
$handle = fopen($instFilePath, "r");
if ($handle) {
    while (($line = fgets($handle)) !== false) {
        $array[] = trim($line);
    }

    fclose($handle);
} else {
    // error opening the file.
} 

$tmpScenario = $array[0];
//$content = $tmpScenario;

foreach ($array as $key => $tmpScenario) {
    foreach ($fss as $keyargs => $fs) {
        $results = getFsiPar10ForScenarioAndCase($fs,$tmpScenario);
        $dic_par10[$tmpScenario][$fs] = $results[0];
        $dic_fsi[$tmpScenario][$fs] = $results[1];
    }

}


//par10
foreach ($array as $key => $tmpScenario) {
    $value_par10 = $dic_par10[$tmpScenario]["original"];
    $value_fsi = $dic_fsi[$tmpScenario]["original"];
    foreach ($fss as $keyargs => $fs) {
        if ($fs != "original") {
            $diff_par10[$tmpScenario][$fs] =  round($dic_par10[$tmpScenario][$fs] - $value_par10,5);
            $diff_fsi[$tmpScenario][$fs] = round($dic_fsi[$tmpScenario][$fs]  - $value_fsi,5);
        }
        
    }
}


//html

//par10

//table heading
$htmlContentpt = "<tr><td><label>Scenario</label></td>";
foreach ($fss as $key => $fs) {
    $htmlContentpt .= "<td><label>$fs</label></td>";
}
$htmlContentpt .= "</tr>";

//table content
foreach ($array as $key => $scenario) {
    $htmlContentpt .= "<tr>";
    $htmlContentpt .= "<td><label>$scenario</label></td>";
    $value_par10 = $dic_par10[$scenario]["original"];
    $htmlContentpt .= "<td>".round($value_par10,5)."</td>";
    foreach ($fss as $keyargs => $fs) {
        if ($fs != "original") {
            $tmpFsPar10 = $diff_par10[$scenario][$fs];
            $htmlContentpt .= ($tmpFsPar10 >= 0)? "<td class='green'>".$tmpFsPar10."</td>" : "<td class='red'>".$tmpFsPar10."</td>";
        }
    }
    $htmlContentpt .= "</tr>";
}


//fsi

$htmlContentfsi = "<tr><td><label>Scenario</label></td>";
foreach ($fss as $key => $fs) {
    $htmlContentfsi .= "<td><label>$fs</label></td>";
}
$htmlContentfsi .= "</tr>";

//table content
foreach ($array as $key => $scenario) {
    $htmlContentfsi .= "<tr>";
    $htmlContentfsi .= "<td><label>$scenario</label></td>";
    $value_fsi_original = $dic_fsi[$scenario]["original"];
    $htmlContentfsi .= "<td>".round($value_fsi_original,5)."</td>";
    foreach ($fss as $keyargs => $fs) {
        if ($fs != "original") {
            $tmpFsFsi = $diff_fsi[$scenario][$fs];
            $htmlContentfsi .= ($tmpFsFsi >= 0)? "<td class='green'>".$tmpFsFsi."</td>" : "<td class='red'>".$tmpFsFsi."</td>";
        }
    }
    $htmlContentfsi .= "</tr>";
}


function getFsiPar10ForScenarioAndCase($scenario,$case){
    // load original
    $originalpath = "data/".$scenario."/".$case.".txt";
    $par10 = array();
    $fsi = array();

    //open file
    $handle = fopen($originalpath, "r");
    if ($handle) {
        while (($line = fgets($handle)) !== false) {
            // process the line read.
            $pos = strrpos($line, "SUNNY PAR10:");
            if ($pos !== false) { // note: three equal signs
                $splitted = split("PAR10:", $line);
                $par10 =  round(floatval($splitted[1]),3);
            }

            $pos = strrpos($line, "SUNNY FSI:");
            if ($pos !== false) { // note: three equal signs
                $splitted = split("FSI:", $line);
                $fsi = round(floatval($splitted[1]),3);
            }
        }

        fclose($handle);
    }
    return array($par10,$fsi);
}


?>


<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>

    <head>
        <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
        <meta charset="utf-8"/>
        <link type='text/css' href='css/bootstrap.css' rel='stylesheet' />
        <script type="text/javascript" src="lib/jquery-1.7.2.min.js"></script>
        <script type='text/javascript' src='lib/bootstrap.min.js'></script>

        <style>
            .content{
                margin: auto;
                width: 70%;
            }
            .green{
                 color: green;
            }
            .red{
                 color: red;
            }
            
        </style>
  </head>

    <body>
        <div class='content'>
        <div class="table-responsive">
            <h2>Par10</h2>
            <table class="table">

             <?php echo $htmlContentpt;?>
         </table>

         <h2>FSI</h2>
         <table class="table">

             <?php echo $htmlContentfsi;?>
         </table>
     </div>
    </body>
    
    
    
<script>
</script>


</html>