<?php
// Setting up the HTML page and aesthetics
echo "<html lang = 'en'>";
echo "<link rel = 'stylesheet' href = 'aesthetics.css'>";	

// Setting up the navigation bar
echo "<body>";
	echo "<nav>";
		echo "<li><a href = 'https://bioinfmsc8.bio.ed.ac.uk/~s2103976/ICA/home.html'>Home</a></li>";
                echo "<li><a href = 'https://bioinfmsc8.bio.ed.ac.uk/~s2103976/ICA/analytis.php'>Analy-tis Tool</a></li>";
                echo "<li><a href = 'https://bioinfmsc8.bio.ed.ac.uk/~s2103976/ICA/about.html'>About</a></li>";
                echo "<li><a href = 'https://bioinfmsc8.bio.ed.ac.uk/~s2103976/ICA/help.html'>Help</a></li>";
                echo "<li><a href = 'https://bioinfmsc8.bio.ed.ac.uk/~s2103976/ICA/statement_of_credit.html'>Statement of Credit</a></li>";
        echo "</nav>";

		echo "<h1>Analy-tis</h1>";
		echo "<h2>This is the Analytis tool, which we will use to conduct our protein analysis</h2>";

		//Setting up the form to retrieve the protein and taxonomic information
		echo "<form action = 'analytis.php' method = 'post'>";
		echo	"<label>1. Specify your protein family: <input type = 'text' name = 'prot_family'></label><br>";
		echo	"<label>2. Specify your taxonomic group:<input type = 'text' name = 'taxon_group'></label><br>";
		echo	"<input type = 'submit' value = 'Submit'>";
		echo "</form>";
echo "</html>";

//Collecting the input from the Analytis form and creating it as output to feed into the backend_python.py file	
		//Using htmlspecialchars to preserve the original html meaning of the code
if(isset($_POST['prot_family']) && isset($_POST['taxon_group'])){
//	$protein_family = escapeshellarg($_POST['prot_family']);
//	$taxonomic_group = escapeshellarg($_POST['taxon_group']);

	$protein_family = preg_replace('/[^a-zA-Z0-9_-]/', '', $_POST['prot_family']);
	$taxonomic_group = preg_replace('/[^a-zA-Z0-9_-]/', '', $_POST['taxon_group']);



	$python_run = "python3 /home/s2103976/public_html/ICA/backend_python.py $protein_family $taxonomic_group";
	$run_python_run = shell_exec($python_run);

	//$formcommand = escapeshellcmd("EMAIL=". escapeshellarg("s2103976@ed.ac.uk") . "python3 backend_python.py" . $protein_family . " " . $taxonomic_group);
	//$formoutput = shell_exec($run_python_run);
	echo $run_python_run;
}

//Part 3: Scan Protein Sequences with PROSITE Motifs to Identify Associated Domains and Generate Reports/Plots
//3.a Login credentials
require_once 'login_credentials.php';

//3a A quick detour to Python stuff
$prosite_tsv = "{$taxonomic_group}_{$protein_family}_data.tsv";
if (file_exists($prosite_tsv)) {
    // Change file permissions (e.g. make it readable/writable by all)
    if (chmod($prosite_tsv, 0777)) {
        echo "Permissions for $prosite_tsv changed successfully.";
    } else {
        echo "Failed to change permissions for $prosite_tsv.";
    }
} else {
    echo "File not found: $prosite_tsv";
}

//3.b taking the form input and creating columns
$colswanted = "";
$counter = 0;
settype($counter, "integer");

foreach ($_POST as $n => $stuff) {
	$counter = $counter + 1;
	if ($counter == 1) {
		$colswanted = $stuff;
	} else {
	$colswanted = $colswanted . "," . $stuff;
	}
}

//3.c Creating a PDO instance
$pdo = new PDO("mysql:host=$server;dbname=$database;charset = utf8mb4",$username,$password);
$pdo -> setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

//3.d Creating MySQL tables
$sql = "CREATE TABLE IF NOT EXISTS fastaland (
	SeqName VARCHAR(255),
	Sequence TEXT NOT NULL, 
	Organism VARCHAR(255))";

//3.e Query database and return results
$sql = "SELECT $colswanted FROM fastaland";
$stmt = $pdo->prepare($sql);
$stmt->execute();
$results = $stmt->fetchAll(PDO::FETCH_ASSOC);

//$pdo -> exec($sql);

//3.d Displaying the MySQL Data in a HTML table
echo "<html>";
echo "<table border = '1'>";
echo "<tr>";

foreach (array_keys($results[0]) as $columnName){
	echo "<th>" . htmlspecialchars($columnName) . "</th>";
}
echo "</tr>";

foreach ($results as $row){
	echo "<tr>";
	foreach ($row as $value) {
		echo "<td>" . htmlspecialchars($value) . "</td>";
	}
	echo"</tr>";
}
echo "</table>";

echo "<form action='analytis.php', method = 'post'>";
echo  "<input type='checkbox' id='test1' name='test1' value='MSA'>";
echo  "<label for='test1'> Multiple Sequence Alignment</label><br>";
echo  "<input type='checkbox' id='test2' name='test2' value='SSP'>";
echo  "<label for='vehicle2'> Secondary Structure Prediction</label><br>";
echo  "<input type='checkbox' id='test3' name='test3' value='PA'>";
echo  "<label for='vehicle3'> Phylogenetic Analysis</label><br><br>";
echo  "<input type='submit' value='Submit'>";
echo "</form>";

echo	"</body>";
echo "</html>";

?>
