<?php
//A function to make a new id for each unique user
function id_maker(){
	if(!isset($_COOKIE['u_'])) {
		$id = 'u_' . uniqid('', true);
                setcookie('u_', $id, time() + (86400 * 30), "/");
                //echo "Welcome to Prot " . $id;
                return $id;
	} else {
		$id = $_COOKIE['u_'];
		//echo "Welcome back " . $id;
                return($id);
	}
}

function motifs_table_maker($pdo){
$pdo -> exec("CREATE TABLE IF NOT EXISTS motifs (
        SeqName VARCHAR(255),
        Start INT NOT NULL,
	End INT NOT NULL,
	Score INT NOT NULL,
	Strand VARCHAR(10),
	Motif TEXT)");
}



?>
