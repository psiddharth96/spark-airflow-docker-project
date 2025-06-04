import sys
from lib import Utils
from lib.logger import Log4j

from lib.ConfigLoader import get_config
from lib.DataLoader import read_accounts_df, read_parties_df, read_party_address_df
from lib.Transformations import apply_header, get_contract,get_relations, get_address, join_contract_party, join_party_address, kafka_df, write_test_data_json

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("Usage: sbdl {local, qa, prod} {load_date} : Arguments are missing")
        sys.exit(-1)

    job_run_env = sys.argv[1].upper()
    load_date = sys.argv[2]

    spark = Utils.get_spark_session(job_run_env)
    logger = Log4j(spark)

    logger.info("Finished creating Spark Session")
    
    logger.info("Loading sbdl app configurations...")
    sbdl_conf = get_config(job_run_env)
    enable_hive = True if sbdl_conf["enable.hive"] == "true" else False
    hive_db = sbdl_conf["hive.database"]
    
    logger.info("Reading Accounts data...")
    accounts_df = read_accounts_df(spark, job_run_env, enable_hive, hive_db)
    contract_id_df = get_contract(accounts_df)
    
    logger.info("Loading data from parties relations csv...")
    parties_df = read_parties_df(spark, job_run_env, enable_hive, hive_db)
    
    logger.info("Transforming data from parties relations df...")
    party_transformed_df = get_relations(parties_df)
    
    logger.info("Loading data from party address csv...")
    party_address_df = read_party_address_df(spark, job_run_env, enable_hive, hive_db)
    
    logger.info("Transforming data from parties address df...")
    address_transformed_df = get_address(party_address_df)
    
    logger.info("Joining party address df...")
    joined_party_df = join_party_address(party_transformed_df, address_transformed_df)
    
    joined_party_df.show(truncate=False)
    
    logger.info("Joining contract address df...")
    joined_contract_df = join_contract_party(contract_id_df, joined_party_df)
    
    logger.info("Applying event header...")
    final_df = apply_header(spark, joined_contract_df)
    
    logger.info("Preparing Kafka df from final df...")
    kafka_df = kafka_df(final_df)
    
    write_test_data_json(spark, kafka_df)
    
    
