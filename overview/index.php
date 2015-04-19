<?

/**
*
*
* A html based visualiser for sunny performance on feature selected dataset
*
*
*/

$instFilePath = "inst.txt";

$content = "";
$scenarios = array();
$handle = fopen($instFilePath, "r");
if ($handle) {
    while (($line = fgets($handle)) !== false) {
        // process the line read.
        //$content .= $line;
        $array[] = trim($line);
    }

    fclose($handle);
} else {
    // error opening the file.
} 

$tmpScenario = $array[0];
//$content = $tmpScenario;

foreach ($array as $key => $tmpScenario) {
    $results = getFsiPar10ForScenarioAndCase("original",$tmpScenario);
    $dic_fsi_original[$tmpScenario] = $results[0];
    $dic_par10_original[$tmpScenario] = $results[1];

    $results = getFsiPar10ForScenarioAndCase("forward",$tmpScenario);
    $dic_fsi_forward[$tmpScenario] = $results[0];
    $dic_par10_forward[$tmpScenario] = $results[1];

    $results = getFsiPar10ForScenarioAndCase("backward",$tmpScenario);
    $dic_fsi_backward[$tmpScenario] = $results[0];
    $dic_par10_backward[$tmpScenario] = $results[1];

    $results = getFsiPar10ForScenarioAndCase("ranker5",$tmpScenario);
    $dic_fsi_ranker5[$tmpScenario] = $results[0];
    $dic_par10_ranker5[$tmpScenario] = $results[1];
}


//par10

//diff par10 forward
$diff_par10_forward = array();
foreach ($dic_par10_original as $key => $value) {
    $diff_par10_forward[$key] = round($dic_par10_forward[$key] - $value,5);
}

//diff fsi forward
$diff_fsi_forward = array();
foreach ($dic_fsi_original as $key => $value) {
   // echo $dic_fsi_forward[$key]." ".$value."<br/>";
    $diff_fsi_forward[$key] = round($dic_fsi_forward[$key] - $value,5);
}

//diff par10 backward
$diff_par10_backward = array();
foreach ($dic_par10_original as $key => $value) {
    $diff_par10_backward[$key] = round($dic_par10_backward[$key] - $value,5);
}

//diff fsi backward
$diff_fsi_backward  = array();
foreach ($dic_fsi_original as $key => $value) {
    $diff_fsi_backward[$key] = round($dic_fsi_backward[$key] - $value,5);
}


//diff par10 ranker5
$diff_par10_ranker5 = array();
foreach ($dic_par10_original as $key => $value) {
    $diff_par10_ranker5[$key] = round($dic_par10_ranker5[$key] - $value,5);
}

//diff fsi ranker5
$diff_fsi_ranker5 = array();
foreach ($dic_fsi_original as $key => $value) {
    $diff_fsi_ranker5[$key] = round($dic_fsi_ranker5[$key] - $value,5);
}


//html

//par10

//table heading
$htmlContentpt = "<tr> <td><label>Scenario</label></td> <td><label>Sunny</label></td> <td><label>fs-forward</label></td> <td><label>fs-backward</label></td> <td><label>ranker5</label></td> </tr>";

//par10
foreach ($dic_par10_original as $key => $value) {
     $htmlContentpt .= "<tr>";
     $htmlContentpt .= "<td> <label>".$key."</label> </td>";

     $htmlContentpt .= "<td>".round($dic_par10_original[$key],5)."</td>";
     $htmlContentpt .= ($diff_par10_forward[$key] >= 0)? "<td class='green'>".$diff_par10_forward[$key]."</td>" : "<td class='red'>".$diff_par10_forward[$key]."</td>";
     $htmlContentpt .= ($diff_par10_backward[$key] >= 0)? "<td class='green'>".$diff_par10_backward[$key]."</td>" : "<td class='red'>".$diff_par10_backward[$key]."</td>";
     $htmlContentpt .= ($diff_par10_ranker5[$key] >= 0)? "<td class='green'>".$diff_par10_ranker5[$key]."</td>" : "<td class='red'>".$diff_par10_ranker5[$key]."</td>";
     $htmlContentpt .= "</tr>";
}


//fsi

//table heading
$htmlContentfsi = "<tr> <td><label>Scenario</label></td> <td><label>Sunny</label></td> <td><label>fs-forward</label></td> <td><label>fs-backward</label></td> <td><label>ranker5</label></td> </tr>";

//par10
foreach ($dic_par10_original as $key => $value) {
     $htmlContentfsi .= "<tr>";
     $htmlContentfsi .= "<td> <label>".$key."</label> </td>";

     $htmlContentfsi .= "<td>".round($dic_fsi_original[$key],5)."</td>";
     $htmlContentfsi .= ($diff_fsi_forward[$key] >= 0)? "<td class='green'>".$diff_fsi_forward[$key]."</td>" : "<td class='red'>".$diff_fsi_forward[$key]."</td>";
     $htmlContentfsi .= ($diff_fsi_backward[$key] >= 0)? "<td class='green'>".$diff_fsi_backward[$key]."</td>" : "<td class='red'>".$diff_fsi_backward[$key]."</td>";
     $htmlContentfsi .= ($diff_fsi_ranker5[$key] >= 0)? "<td class='green'>".$diff_fsi_ranker5[$key]."</td>" : "<td class='red'>".$diff_fsi_ranker5[$key]."</td>";
     $htmlContentfsi .= "</tr>";
}

// //html head
// $htmlContent .= "<tr>";
// foreach ($dic_par10_original as $key => $value) {
//      $htmlContent .= "<td> <label>".$key."</label> </td>";
// }
// $htmlContent .= "</tr>";

// //construct par10 table
// $htmlContent .= "<tr>";
// foreach ($dic_par10_original as $key => $value) {
//      $htmlContent .= "<td>".$diff_par10_forward[$key]."</td>";
// }
// $htmlContent .= "</tr>";

//var_dump($diff_par10_forward);
//var_dump($diff_fsi_forward);

function getFsiPar10ForScenarioAndCase($scenario,$case){
    // load original
    $originalpath = "data/".$scenario."/".$case.".txt";
    $dic_fsi_original = array();
    $dic_par10_original = array();

    //open file
    $handle = fopen($originalpath, "r");
    if ($handle) {
        while (($line = fgets($handle)) !== false) {
            // process the line read.
            $pos = strrpos($line, "SUNNY PAR10:");
            if ($pos !== false) { // note: three equal signs
                $splitted = split("PAR10:", $line);
                $par10 = $splitted[1];
            }

            $pos = strrpos($line, "SUNNY FSI:");
            if ($pos !== false) { // note: three equal signs
                $splitted = split("FSI:", $line);
                $fsi = $splitted[1];
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