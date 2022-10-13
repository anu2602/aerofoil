CREATE TABLE aerofoil_backfill (
	id serial primary key, 
	dag_id varchar(250) not null, 
	task_regex varchar(250),
	start_date date not null,
	end_date date not null,
	clear_previous boolean,
	rerun_failed boolean,
	run_backwards boolean,
	mark_success boolean,
	status varchar(10) not null,
	
	ti_dag_id varchar(250),
	ti_task_id varchar(250),
	ti_run_id varchar(250),
	ti_map_id Integer,
	cmd varchar(500),

	started_at timestamp,
	started_by varchar(64),
	terminated_at timestamp,
	terminated_by varchar(64)
)

CREATE TABLE aerofoil_reset_dag(
	id serial primary key,
	dag_id varchar(250) not null,
	reset_type varchar(20) not null,
	reset_by varchar(10) not null,
	reset_date date not null,
	reset_reason varchar(200)
)
