select id_rep, id_dishr, quantity, cost, year_, month_ from reports
where year_ = $date_start and month_ = $date_end