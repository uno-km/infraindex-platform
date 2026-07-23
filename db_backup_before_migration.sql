--
-- PostgreSQL database dump
--

\restrict Gpr1CzDpQNBgaIOiOQBTAgXfnuQ5NGmVh99qYpHetthyQxXvcOCRP4eYhudlOpQ

-- Dumped from database version 16.14
-- Dumped by pg_dump version 16.14

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE ONLY public.storage_tiers DROP CONSTRAINT storage_tiers_provider_id_fkey;
ALTER TABLE ONLY public.source_attributions DROP CONSTRAINT source_attributions_license_id_fkey;
ALTER TABLE ONLY public.provider_regions DROP CONSTRAINT provider_regions_provider_id_fkey;
ALTER TABLE ONLY public.pricing_plans DROP CONSTRAINT pricing_plans_offering_id_fkey;
ALTER TABLE ONLY public.price_observations DROP CONSTRAINT price_observations_pricing_plan_id_fkey;
ALTER TABLE ONLY public.price_alerts DROP CONSTRAINT price_alerts_gpu_model_id_fkey;
ALTER TABLE ONLY public.offering_gpu_configurations DROP CONSTRAINT offering_gpu_configurations_offering_id_fkey;
ALTER TABLE ONLY public.offering_gpu_configurations DROP CONSTRAINT offering_gpu_configurations_gpu_variant_id_fkey;
ALTER TABLE ONLY public.offering_cpu_configurations DROP CONSTRAINT offering_cpu_configurations_offering_id_fkey;
ALTER TABLE ONLY public.offering_cpu_configurations DROP CONSTRAINT offering_cpu_configurations_cpu_variant_id_fkey;
ALTER TABLE ONLY public.memory_modules DROP CONSTRAINT memory_modules_manufacturer_id_fkey;
ALTER TABLE ONLY public.instance_offerings DROP CONSTRAINT instance_offerings_region_id_fkey;
ALTER TABLE ONLY public.instance_offerings DROP CONSTRAINT instance_offerings_provider_id_fkey;
ALTER TABLE ONLY public.gpu_variants DROP CONSTRAINT gpu_variants_model_id_fkey;
ALTER TABLE ONLY public.gpu_models DROP CONSTRAINT gpu_models_manufacturer_id_fkey;
ALTER TABLE ONLY public.cpu_variants DROP CONSTRAINT cpu_variants_model_id_fkey;
ALTER TABLE ONLY public.cpu_models DROP CONSTRAINT cpu_models_manufacturer_id_fkey;
ALTER TABLE ONLY public."SYS_CD_BAS" DROP CONSTRAINT "SYS_CD_BAS_SYS_GROUP_ID_fkey";
DROP INDEX public.ix_tbl_rtl_prc_hist_ts;
DROP INDEX public.ix_tbl_rtl_prc_hist_pltf_nm;
DROP INDEX public.ix_tbl_rtl_prc_hist_mdl_nm;
DROP INDEX public.ix_tbl_obx_evt_tpc_nm;
DROP INDEX public.ix_tbl_obx_evt_proc_st;
DROP INDEX public.ix_tbl_news_arti_src_nm;
DROP INDEX public.ix_tbl_news_arti_pub_ts;
DROP INDEX public.ix_tbl_news_arti_crt_ts;
DROP INDEX public.ix_tbl_news_arti_arti_url;
DROP INDEX public.ix_tbl_gpu_prc_hist_ts;
DROP INDEX public.ix_tbl_gpu_prc_hist_prv_id;
DROP INDEX public.ix_tbl_gpu_prc_hist_gpu_mdl;
DROP INDEX public.ix_tbl_gpu_prc_hist_cpu_mdl;
DROP INDEX public.ix_tbl_fin_mkt_hist_ts;
DROP INDEX public.ix_tbl_fin_mkt_hist_sym_cd;
DROP INDEX public.ix_tbl_fin_mkt_hist_ast_typ;
DROP INDEX public.ix_storage_tiers_provider_id;
DROP INDEX public.ix_storage_providers_name;
DROP INDEX public.ix_source_attributions_provider_id;
DROP INDEX public.ix_schedule_configs_provider_id;
DROP INDEX public.ix_providers_slug;
DROP INDEX public.ix_providers_name;
DROP INDEX public.ix_provider_regions_provider_region_id;
DROP INDEX public.ix_provider_regions_provider_id;
DROP INDEX public.ix_pricing_plans_offering_id;
DROP INDEX public.ix_price_observations_pricing_plan_id;
DROP INDEX public.ix_price_alerts_user_email;
DROP INDEX public.ix_price_alerts_gpu_model_id;
DROP INDEX public.ix_offering_gpu_configurations_offering_id;
DROP INDEX public.ix_offering_gpu_configurations_gpu_variant_id;
DROP INDEX public.ix_offering_cpu_configurations_offering_id;
DROP INDEX public.ix_offering_cpu_configurations_cpu_variant_id;
DROP INDEX public.ix_memory_modules_manufacturer_id;
DROP INDEX public.ix_memory_manufacturers_name;
DROP INDEX public.ix_instance_offerings_region_id;
DROP INDEX public.ix_instance_offerings_provider_id;
DROP INDEX public.ix_instance_offerings_machine_type_name;
DROP INDEX public.ix_idempotency_keys_key;
DROP INDEX public.ix_gpu_variants_model_id;
DROP INDEX public.ix_gpu_models_manufacturer_id;
DROP INDEX public.ix_data_quality_issues_run_id;
DROP INDEX public.ix_data_quality_issues_observation_id;
DROP INDEX public.ix_cpu_variants_model_id;
DROP INDEX public.ix_cpu_models_manufacturer_id;
DROP INDEX public.ix_collection_runs_provider_started;
DROP INDEX public.ix_collection_runs_provider_id;
DROP INDEX public.idx_rtl_prc_pltf_mdl_ts;
DROP INDEX public.idx_rtl_prc_hw_mdl_ts;
DROP INDEX public.idx_news_arti_pub_src;
DROP INDEX public.idx_gpu_prc_prv_ts;
DROP INDEX public.idx_gpu_prc_mdl_ts;
DROP INDEX public.idx_fin_mkt_sym_ts;
ALTER TABLE ONLY public.tbl_rtl_prc_hist DROP CONSTRAINT tbl_rtl_prc_hist_pkey;
ALTER TABLE ONLY public.tbl_obx_evt DROP CONSTRAINT tbl_obx_evt_pkey;
ALTER TABLE ONLY public.tbl_news_arti DROP CONSTRAINT tbl_news_arti_pkey;
ALTER TABLE ONLY public.tbl_gpu_prc_hist DROP CONSTRAINT tbl_gpu_prc_hist_pkey;
ALTER TABLE ONLY public.tbl_fin_mkt_hist DROP CONSTRAINT tbl_fin_mkt_hist_pkey;
ALTER TABLE ONLY public.storage_tiers DROP CONSTRAINT storage_tiers_pkey;
ALTER TABLE ONLY public.storage_providers DROP CONSTRAINT storage_providers_pkey;
ALTER TABLE ONLY public.source_attributions DROP CONSTRAINT source_attributions_pkey;
ALTER TABLE ONLY public.schedule_configs DROP CONSTRAINT schedule_configs_pkey;
ALTER TABLE ONLY public.providers DROP CONSTRAINT providers_pkey;
ALTER TABLE ONLY public.provider_regions DROP CONSTRAINT provider_regions_pkey;
ALTER TABLE ONLY public.pricing_plans DROP CONSTRAINT pricing_plans_pkey;
ALTER TABLE ONLY public.price_observations DROP CONSTRAINT price_observations_pkey;
ALTER TABLE ONLY public.price_alerts DROP CONSTRAINT price_alerts_pkey;
ALTER TABLE ONLY public.offering_gpu_configurations DROP CONSTRAINT offering_gpu_configurations_pkey;
ALTER TABLE ONLY public.offering_cpu_configurations DROP CONSTRAINT offering_cpu_configurations_pkey;
ALTER TABLE ONLY public.memory_modules DROP CONSTRAINT memory_modules_pkey;
ALTER TABLE ONLY public.memory_manufacturers DROP CONSTRAINT memory_manufacturers_pkey;
ALTER TABLE ONLY public.instance_offerings DROP CONSTRAINT instance_offerings_pkey;
ALTER TABLE ONLY public.idempotency_keys DROP CONSTRAINT idempotency_keys_pkey;
ALTER TABLE ONLY public.gpu_variants DROP CONSTRAINT gpu_variants_pkey;
ALTER TABLE ONLY public.gpu_models DROP CONSTRAINT gpu_models_pkey;
ALTER TABLE ONLY public.gpu_models DROP CONSTRAINT gpu_models_name_key;
ALTER TABLE ONLY public.gpu_manufacturers DROP CONSTRAINT gpu_manufacturers_pkey;
ALTER TABLE ONLY public.gpu_manufacturers DROP CONSTRAINT gpu_manufacturers_name_key;
ALTER TABLE ONLY public.data_quality_issues DROP CONSTRAINT data_quality_issues_pkey;
ALTER TABLE ONLY public.data_licenses DROP CONSTRAINT data_licenses_pkey;
ALTER TABLE ONLY public.cpu_variants DROP CONSTRAINT cpu_variants_pkey;
ALTER TABLE ONLY public.cpu_models DROP CONSTRAINT cpu_models_pkey;
ALTER TABLE ONLY public.cpu_models DROP CONSTRAINT cpu_models_name_key;
ALTER TABLE ONLY public.cpu_manufacturers DROP CONSTRAINT cpu_manufacturers_pkey;
ALTER TABLE ONLY public.cpu_manufacturers DROP CONSTRAINT cpu_manufacturers_name_key;
ALTER TABLE ONLY public.collection_runs DROP CONSTRAINT collection_runs_pkey;
ALTER TABLE ONLY public.alembic_version DROP CONSTRAINT alembic_version_pkc;
ALTER TABLE ONLY public."SYS_CD_GROUP_BAS" DROP CONSTRAINT "SYS_CD_GROUP_BAS_pkey";
ALTER TABLE ONLY public."SYS_CD_BAS" DROP CONSTRAINT "SYS_CD_BAS_pkey";
DROP TABLE public.tbl_rtl_prc_hist;
DROP TABLE public.tbl_obx_evt;
DROP TABLE public.tbl_news_arti;
DROP TABLE public.tbl_gpu_prc_hist;
DROP TABLE public.tbl_fin_mkt_hist;
DROP TABLE public.storage_tiers;
DROP TABLE public.storage_providers;
DROP TABLE public.source_attributions;
DROP TABLE public.schedule_configs;
DROP TABLE public.providers;
DROP TABLE public.provider_regions;
DROP TABLE public.pricing_plans;
DROP TABLE public.price_observations;
DROP TABLE public.price_alerts;
DROP TABLE public.offering_gpu_configurations;
DROP TABLE public.offering_cpu_configurations;
DROP TABLE public.memory_modules;
DROP TABLE public.memory_manufacturers;
DROP TABLE public.instance_offerings;
DROP TABLE public.idempotency_keys;
DROP TABLE public.gpu_variants;
DROP TABLE public.gpu_models;
DROP TABLE public.gpu_manufacturers;
DROP TABLE public.data_quality_issues;
DROP TABLE public.data_licenses;
DROP TABLE public.cpu_variants;
DROP TABLE public.cpu_models;
DROP TABLE public.cpu_manufacturers;
DROP TABLE public.collection_runs;
DROP TABLE public.alembic_version;
DROP TABLE public."SYS_CD_GROUP_BAS";
DROP TABLE public."SYS_CD_BAS";
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: SYS_CD_BAS; Type: TABLE; Schema: public; Owner: infraindex
--

CREATE TABLE public."SYS_CD_BAS" (
    "SYS_GROUP_ID" character varying(50) NOT NULL,
    "SYS_CD_ID" character varying(50) NOT NULL,
    "SYS_CD_NM" character varying(100) NOT NULL,
    "CRT_DT" timestamp with time zone DEFAULT now() NOT NULL,
    "UPD_DT" timestamp with time zone DEFAULT now() NOT NULL,
    "DESC_TXT" text,
    "REF_VAL_1" character varying(200),
    "REF_VAL_2" character varying(200),
    "REF_VAL_3" character varying(200),
    "REF_VAL_4" character varying(200),
    "REF_VAL_5" character varying(200),
    "REF_VAL_6" character varying(200),
    "REF_VAL_7" character varying(200),
    "REF_VAL_8" character varying(200),
    "REF_VAL_9" character varying(200),
    "REF_VAL_10" character varying(200)
);


ALTER TABLE public."SYS_CD_BAS" OWNER TO infraindex;

--
-- Name: SYS_CD_GROUP_BAS; Type: TABLE; Schema: public; Owner: infraindex
--

CREATE TABLE public."SYS_CD_GROUP_BAS" (
    "SYS_GROUP_ID" character varying(50) NOT NULL,
    "GRP_NM" character varying(100) NOT NULL,
    "CRT_DT" timestamp with time zone DEFAULT now() NOT NULL,
    "UPD_DT" timestamp with time zone DEFAULT now() NOT NULL,
    "DESC_TXT" text,
    "REF_VAL_1" character varying(200),
    "REF_VAL_2" character varying(200),
    "REF_VAL_3" character varying(200),
    "REF_VAL_4" character varying(200),
    "REF_VAL_5" character varying(200),
    "REF_VAL_6" character varying(200),
    "REF_VAL_7" character varying(200),
    "REF_VAL_8" character varying(200),
    "REF_VAL_9" character varying(200),
    "REF_VAL_10" character varying(200)
);


ALTER TABLE public."SYS_CD_GROUP_BAS" OWNER TO infraindex;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: infraindex
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO infraindex;

--
-- Name: collection_runs; Type: TABLE; Schema: public; Owner: infraindex
--

CREATE TABLE public.collection_runs (
    provider_id character varying(50) NOT NULL,
    started_at timestamp with time zone NOT NULL,
    completed_at timestamp with time zone,
    status character varying(50) NOT NULL,
    items_collected integer NOT NULL,
    error_message text,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.collection_runs OWNER TO infraindex;

--
-- Name: cpu_manufacturers; Type: TABLE; Schema: public; Owner: infraindex
--

CREATE TABLE public.cpu_manufacturers (
    name character varying(255) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.cpu_manufacturers OWNER TO infraindex;

--
-- Name: cpu_models; Type: TABLE; Schema: public; Owner: infraindex
--

CREATE TABLE public.cpu_models (
    manufacturer_id uuid NOT NULL,
    name character varying(255) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.cpu_models OWNER TO infraindex;

--
-- Name: cpu_variants; Type: TABLE; Schema: public; Owner: infraindex
--

CREATE TABLE public.cpu_variants (
    model_id uuid NOT NULL,
    name character varying(255) NOT NULL,
    cores integer NOT NULL,
    threads integer NOT NULL,
    base_clock_ghz double precision,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.cpu_variants OWNER TO infraindex;

--
-- Name: data_licenses; Type: TABLE; Schema: public; Owner: infraindex
--

CREATE TABLE public.data_licenses (
    name character varying(255) NOT NULL,
    version character varying(50),
    collection_allowed boolean NOT NULL,
    public_display_allowed boolean NOT NULL,
    redistribution_allowed boolean NOT NULL,
    attribution_required boolean NOT NULL,
    notes text,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.data_licenses OWNER TO infraindex;

--
-- Name: data_quality_issues; Type: TABLE; Schema: public; Owner: infraindex
--

CREATE TABLE public.data_quality_issues (
    run_id character varying(36),
    observation_id character varying(36),
    issue_type character varying(100) NOT NULL,
    severity character varying(50) NOT NULL,
    description text NOT NULL,
    raw_data_snapshot text,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.data_quality_issues OWNER TO infraindex;

--
-- Name: gpu_manufacturers; Type: TABLE; Schema: public; Owner: infraindex
--

CREATE TABLE public.gpu_manufacturers (
    name character varying(255) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.gpu_manufacturers OWNER TO infraindex;

--
-- Name: gpu_models; Type: TABLE; Schema: public; Owner: infraindex
--

CREATE TABLE public.gpu_models (
    manufacturer_id uuid NOT NULL,
    name character varying(255) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.gpu_models OWNER TO infraindex;

--
-- Name: gpu_variants; Type: TABLE; Schema: public; Owner: infraindex
--

CREATE TABLE public.gpu_variants (
    model_id uuid NOT NULL,
    name character varying(255) NOT NULL,
    form_factor character varying(50),
    vram_gb double precision NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.gpu_variants OWNER TO infraindex;

--
-- Name: idempotency_keys; Type: TABLE; Schema: public; Owner: infraindex
--

CREATE TABLE public.idempotency_keys (
    key character varying(255) NOT NULL,
    job_name character varying(255) NOT NULL,
    executed_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.idempotency_keys OWNER TO infraindex;

--
-- Name: instance_offerings; Type: TABLE; Schema: public; Owner: infraindex
--

CREATE TABLE public.instance_offerings (
    provider_id uuid NOT NULL,
    region_id uuid,
    machine_type_name character varying(255) NOT NULL,
    includes_cpu boolean NOT NULL,
    includes_ram boolean NOT NULL,
    includes_local_storage boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.instance_offerings OWNER TO infraindex;

--
-- Name: memory_manufacturers; Type: TABLE; Schema: public; Owner: infraindex
--

CREATE TABLE public.memory_manufacturers (
    name character varying(255) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.memory_manufacturers OWNER TO infraindex;

--
-- Name: memory_modules; Type: TABLE; Schema: public; Owner: infraindex
--

CREATE TABLE public.memory_modules (
    manufacturer_id uuid NOT NULL,
    type character varying(50) NOT NULL,
    capacity_gb double precision NOT NULL,
    speed_mhz integer,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.memory_modules OWNER TO infraindex;

--
-- Name: offering_cpu_configurations; Type: TABLE; Schema: public; Owner: infraindex
--

CREATE TABLE public.offering_cpu_configurations (
    offering_id uuid NOT NULL,
    cpu_variant_id uuid NOT NULL,
    count integer NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.offering_cpu_configurations OWNER TO infraindex;

--
-- Name: offering_gpu_configurations; Type: TABLE; Schema: public; Owner: infraindex
--

CREATE TABLE public.offering_gpu_configurations (
    offering_id uuid NOT NULL,
    gpu_variant_id uuid NOT NULL,
    count integer NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.offering_gpu_configurations OWNER TO infraindex;

--
-- Name: price_alerts; Type: TABLE; Schema: public; Owner: infraindex
--

CREATE TABLE public.price_alerts (
    user_email character varying(255) NOT NULL,
    gpu_model_id uuid,
    target_price numeric(16,6) NOT NULL,
    is_active boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.price_alerts OWNER TO infraindex;

--
-- Name: price_observations; Type: TABLE; Schema: public; Owner: infraindex
--

CREATE TABLE public.price_observations (
    pricing_plan_id uuid NOT NULL,
    source_price numeric(16,6) NOT NULL,
    source_currency character varying(3) NOT NULL,
    source_unit character varying(50) NOT NULL,
    normalized_hourly_price numeric(16,6) NOT NULL,
    normalized_gpu_hour_price numeric(16,6) NOT NULL,
    normalized_vram_gb_hour_price numeric(16,6) NOT NULL,
    normalized_monthly_price numeric(16,6) NOT NULL,
    availability_status character varying(50) NOT NULL,
    collected_at timestamp with time zone NOT NULL,
    source_url character varying(1024),
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.price_observations OWNER TO infraindex;

--
-- Name: pricing_plans; Type: TABLE; Schema: public; Owner: infraindex
--

CREATE TABLE public.pricing_plans (
    offering_id uuid NOT NULL,
    plan_type character varying(50) NOT NULL,
    billing_increment_seconds integer NOT NULL,
    minimum_billing_seconds integer NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.pricing_plans OWNER TO infraindex;

--
-- Name: provider_regions; Type: TABLE; Schema: public; Owner: infraindex
--

CREATE TABLE public.provider_regions (
    provider_id uuid NOT NULL,
    provider_region_id character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    country character varying(2),
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.provider_regions OWNER TO infraindex;

--
-- Name: providers; Type: TABLE; Schema: public; Owner: infraindex
--

CREATE TABLE public.providers (
    name character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    official_homepage character varying(1024),
    is_active boolean NOT NULL,
    notes text,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.providers OWNER TO infraindex;

--
-- Name: schedule_configs; Type: TABLE; Schema: public; Owner: infraindex
--

CREATE TABLE public.schedule_configs (
    provider_id character varying(255) NOT NULL,
    cron_expression character varying(50) NOT NULL,
    timezone character varying(50) NOT NULL,
    enabled boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.schedule_configs OWNER TO infraindex;

--
-- Name: source_attributions; Type: TABLE; Schema: public; Owner: infraindex
--

CREATE TABLE public.source_attributions (
    provider_id character varying(255) NOT NULL,
    license_id uuid NOT NULL,
    attribution_text text NOT NULL,
    official_source_url character varying(1024) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.source_attributions OWNER TO infraindex;

--
-- Name: storage_providers; Type: TABLE; Schema: public; Owner: infraindex
--

CREATE TABLE public.storage_providers (
    name character varying(255) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.storage_providers OWNER TO infraindex;

--
-- Name: storage_tiers; Type: TABLE; Schema: public; Owner: infraindex
--

CREATE TABLE public.storage_tiers (
    provider_id uuid NOT NULL,
    name character varying(255) NOT NULL,
    price_per_gb_month double precision NOT NULL,
    egress_price_per_gb double precision NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.storage_tiers OWNER TO infraindex;

--
-- Name: tbl_fin_mkt_hist; Type: TABLE; Schema: public; Owner: infraindex
--

CREATE TABLE public.tbl_fin_mkt_hist (
    ast_typ character varying(50) NOT NULL,
    sym_cd character varying(100) NOT NULL,
    opn_prc double precision NOT NULL,
    hi_prc double precision NOT NULL,
    lo_prc double precision NOT NULL,
    cls_prc double precision NOT NULL,
    vol_cnt double precision,
    crncy_cd character varying(10) NOT NULL,
    ts timestamp with time zone DEFAULT now() NOT NULL,
    id uuid NOT NULL
);


ALTER TABLE public.tbl_fin_mkt_hist OWNER TO infraindex;

--
-- Name: tbl_gpu_prc_hist; Type: TABLE; Schema: public; Owner: infraindex
--

CREATE TABLE public.tbl_gpu_prc_hist (
    prv_id character varying(50) NOT NULL,
    hw_typ character varying(20) NOT NULL,
    gpu_mdl character varying(100),
    vram_gb numeric(8,2),
    cpu_mdl character varying(100),
    core_cnt numeric(8,2),
    prc_ph numeric(12,6) NOT NULL,
    avl_st character varying(50) NOT NULL,
    prv_url character varying(500),
    sys_ram numeric(8,2),
    tdp_w numeric(8,2),
    ts timestamp with time zone DEFAULT now() NOT NULL,
    id uuid NOT NULL
);


ALTER TABLE public.tbl_gpu_prc_hist OWNER TO infraindex;

--
-- Name: tbl_news_arti; Type: TABLE; Schema: public; Owner: infraindex
--

CREATE TABLE public.tbl_news_arti (
    titl_nm character varying(500) NOT NULL,
    arti_url character varying(1000) NOT NULL,
    src_nm character varying(100) NOT NULL,
    pub_ts timestamp with time zone NOT NULL,
    sum_txt text,
    kwd_txt character varying(500),
    clct_tr character varying(50),
    crt_ts timestamp with time zone DEFAULT now() NOT NULL,
    id uuid NOT NULL
);


ALTER TABLE public.tbl_news_arti OWNER TO infraindex;

--
-- Name: tbl_obx_evt; Type: TABLE; Schema: public; Owner: infraindex
--

CREATE TABLE public.tbl_obx_evt (
    tpc_nm character varying(255) NOT NULL,
    evt_typ character varying(255) NOT NULL,
    payld_dat json NOT NULL,
    crt_ts timestamp with time zone DEFAULT now() NOT NULL,
    proc_st boolean NOT NULL,
    proc_ts timestamp with time zone,
    id uuid NOT NULL
);


ALTER TABLE public.tbl_obx_evt OWNER TO infraindex;

--
-- Name: tbl_rtl_prc_hist; Type: TABLE; Schema: public; Owner: infraindex
--

CREATE TABLE public.tbl_rtl_prc_hist (
    pltf_nm character varying(50) NOT NULL,
    hw_typ character varying(20) NOT NULL,
    mfg_nm character varying(50),
    mdl_nm character varying(200) NOT NULL,
    capa_gb numeric(8,2),
    prc_amt numeric(15,2) NOT NULL,
    crncy_cd character varying(10) NOT NULL,
    prd_url character varying(1000),
    is_offc boolean NOT NULL,
    ts timestamp with time zone DEFAULT now() NOT NULL,
    id uuid NOT NULL
);


ALTER TABLE public.tbl_rtl_prc_hist OWNER TO infraindex;

--
-- Data for Name: SYS_CD_BAS; Type: TABLE DATA; Schema: public; Owner: infraindex
--

COPY public."SYS_CD_BAS" ("SYS_GROUP_ID", "SYS_CD_ID", "SYS_CD_NM", "CRT_DT", "UPD_DT", "DESC_TXT", "REF_VAL_1", "REF_VAL_2", "REF_VAL_3", "REF_VAL_4", "REF_VAL_5", "REF_VAL_6", "REF_VAL_7", "REF_VAL_8", "REF_VAL_9", "REF_VAL_10") FROM stdin;
GPU_PROVIDER	VAST_AI	Vast.ai (P2P)	2026-07-23 03:05:11.397903+00	2026-07-23 03:05:11.397903+00	\N	vast-ai	\N	\N	\N	\N	\N	\N	\N	\N	\N
GPU_PROVIDER	RUNPOD	RunPod	2026-07-23 03:05:11.397903+00	2026-07-23 03:05:11.397903+00	\N	runpod	\N	\N	\N	\N	\N	\N	\N	\N	\N
GPU_PROVIDER	AWS	Amazon Web Services	2026-07-23 03:05:11.397903+00	2026-07-23 03:05:11.397903+00	\N	aws	\N	\N	\N	\N	\N	\N	\N	\N	\N
GPU_PROVIDER	VESSL	VESSL AI	2026-07-23 03:05:11.397903+00	2026-07-23 03:05:11.397903+00	\N	vessl	\N	\N	\N	\N	\N	\N	\N	\N	\N
GPU_PROVIDER	GPUAAS	GPUaaS (한국)	2026-07-23 03:05:11.397903+00	2026-07-23 03:05:11.397903+00	\N	gpuaas	\N	\N	\N	\N	\N	\N	\N	\N	\N
GPU_PROVIDER	CLOUDV	CloudV (한국)	2026-07-23 03:05:11.397903+00	2026-07-23 03:05:11.397903+00	\N	cloudv	\N	\N	\N	\N	\N	\N	\N	\N	\N
GPU_PROVIDER	RUNYOURAI	RunYourAI (한국)	2026-07-23 03:05:11.397903+00	2026-07-23 03:05:11.397903+00	\N	runyourai	\N	\N	\N	\N	\N	\N	\N	\N	\N
GPU_PROVIDER	GABIA	Gabia (한국)	2026-07-23 03:05:11.397903+00	2026-07-23 03:05:11.397903+00	\N	gabia	\N	\N	\N	\N	\N	\N	\N	\N	\N
GPU_PROVIDER	KTCLOUD	KT Cloud (한국)	2026-07-23 03:05:11.397903+00	2026-07-23 03:05:11.397903+00	\N	ktcloud	\N	\N	\N	\N	\N	\N	\N	\N	\N
GPU_PROVIDER	XESKTOP	Xesktop (한국)	2026-07-23 03:05:11.397903+00	2026-07-23 03:05:11.397903+00	\N	xesktop	\N	\N	\N	\N	\N	\N	\N	\N	\N
GPU_PROVIDER	NCLOUD	Naver Cloud (한국)	2026-07-23 03:05:11.397903+00	2026-07-23 03:05:11.397903+00	\N	ncloud	\N	\N	\N	\N	\N	\N	\N	\N	\N
\.


--
-- Data for Name: SYS_CD_GROUP_BAS; Type: TABLE DATA; Schema: public; Owner: infraindex
--

COPY public."SYS_CD_GROUP_BAS" ("SYS_GROUP_ID", "GRP_NM", "CRT_DT", "UPD_DT", "DESC_TXT", "REF_VAL_1", "REF_VAL_2", "REF_VAL_3", "REF_VAL_4", "REF_VAL_5", "REF_VAL_6", "REF_VAL_7", "REF_VAL_8", "REF_VAL_9", "REF_VAL_10") FROM stdin;
GPU_PROVIDER	글로벌 GPU 클라우드 프로바이더	2026-07-23 03:05:11.397903+00	2026-07-23 03:05:11.397903+00	크롤링 및 시세 연동 대상 벤더 목록	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: infraindex
--

COPY public.alembic_version (version_num) FROM stdin;
ba50dd389d86
\.


--
-- Data for Name: collection_runs; Type: TABLE DATA; Schema: public; Owner: infraindex
--

COPY public.collection_runs (provider_id, started_at, completed_at, status, items_collected, error_message, id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: cpu_manufacturers; Type: TABLE DATA; Schema: public; Owner: infraindex
--

COPY public.cpu_manufacturers (name, id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: cpu_models; Type: TABLE DATA; Schema: public; Owner: infraindex
--

COPY public.cpu_models (manufacturer_id, name, id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: cpu_variants; Type: TABLE DATA; Schema: public; Owner: infraindex
--

COPY public.cpu_variants (model_id, name, cores, threads, base_clock_ghz, id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: data_licenses; Type: TABLE DATA; Schema: public; Owner: infraindex
--

COPY public.data_licenses (name, version, collection_allowed, public_display_allowed, redistribution_allowed, attribution_required, notes, id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: data_quality_issues; Type: TABLE DATA; Schema: public; Owner: infraindex
--

COPY public.data_quality_issues (run_id, observation_id, issue_type, severity, description, raw_data_snapshot, id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: gpu_manufacturers; Type: TABLE DATA; Schema: public; Owner: infraindex
--

COPY public.gpu_manufacturers (name, id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: gpu_models; Type: TABLE DATA; Schema: public; Owner: infraindex
--

COPY public.gpu_models (manufacturer_id, name, id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: gpu_variants; Type: TABLE DATA; Schema: public; Owner: infraindex
--

COPY public.gpu_variants (model_id, name, form_factor, vram_gb, id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: idempotency_keys; Type: TABLE DATA; Schema: public; Owner: infraindex
--

COPY public.idempotency_keys (key, job_name, executed_at, id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: instance_offerings; Type: TABLE DATA; Schema: public; Owner: infraindex
--

COPY public.instance_offerings (provider_id, region_id, machine_type_name, includes_cpu, includes_ram, includes_local_storage, id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: memory_manufacturers; Type: TABLE DATA; Schema: public; Owner: infraindex
--

COPY public.memory_manufacturers (name, id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: memory_modules; Type: TABLE DATA; Schema: public; Owner: infraindex
--

COPY public.memory_modules (manufacturer_id, type, capacity_gb, speed_mhz, id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: offering_cpu_configurations; Type: TABLE DATA; Schema: public; Owner: infraindex
--

COPY public.offering_cpu_configurations (offering_id, cpu_variant_id, count, id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: offering_gpu_configurations; Type: TABLE DATA; Schema: public; Owner: infraindex
--

COPY public.offering_gpu_configurations (offering_id, gpu_variant_id, count, id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: price_alerts; Type: TABLE DATA; Schema: public; Owner: infraindex
--

COPY public.price_alerts (user_email, gpu_model_id, target_price, is_active, id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: price_observations; Type: TABLE DATA; Schema: public; Owner: infraindex
--

COPY public.price_observations (pricing_plan_id, source_price, source_currency, source_unit, normalized_hourly_price, normalized_gpu_hour_price, normalized_vram_gb_hour_price, normalized_monthly_price, availability_status, collected_at, source_url, id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: pricing_plans; Type: TABLE DATA; Schema: public; Owner: infraindex
--

COPY public.pricing_plans (offering_id, plan_type, billing_increment_seconds, minimum_billing_seconds, id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: provider_regions; Type: TABLE DATA; Schema: public; Owner: infraindex
--

COPY public.provider_regions (provider_id, provider_region_id, name, country, id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: providers; Type: TABLE DATA; Schema: public; Owner: infraindex
--

COPY public.providers (name, slug, official_homepage, is_active, notes, id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: schedule_configs; Type: TABLE DATA; Schema: public; Owner: infraindex
--

COPY public.schedule_configs (provider_id, cron_expression, timezone, enabled, id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: source_attributions; Type: TABLE DATA; Schema: public; Owner: infraindex
--

COPY public.source_attributions (provider_id, license_id, attribution_text, official_source_url, id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: storage_providers; Type: TABLE DATA; Schema: public; Owner: infraindex
--

COPY public.storage_providers (name, id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: storage_tiers; Type: TABLE DATA; Schema: public; Owner: infraindex
--

COPY public.storage_tiers (provider_id, name, price_per_gb_month, egress_price_per_gb, id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: tbl_fin_mkt_hist; Type: TABLE DATA; Schema: public; Owner: infraindex
--

COPY public.tbl_fin_mkt_hist (ast_typ, sym_cd, opn_prc, hi_prc, lo_prc, cls_prc, vol_cnt, crncy_cd, ts, id) FROM stdin;
\.


--
-- Data for Name: tbl_gpu_prc_hist; Type: TABLE DATA; Schema: public; Owner: infraindex
--

COPY public.tbl_gpu_prc_hist (prv_id, hw_typ, gpu_mdl, vram_gb, cpu_mdl, core_cnt, prc_ph, avl_st, prv_url, sys_ram, tdp_w, ts, id) FROM stdin;
aws	gpu	T4	16.00	\N	\N	0.925000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 16:50:59+00	e6b889d4-c9ab-43a1-9ba1-6f470e2b7141
aws	gpu	A10G	24.00	\N	\N	1.996900	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 16:50:59+00	cd5b2a75-ad7c-4a58-8cba-3ce0c1a5cfe1
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 16:50:59+00	bd869df1-ba99-43e9-af2f-dddd45d0dcfd
aws	gpu	A10G	24.00	\N	\N	3.010100	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 16:50:59+00	2e50da0d-095f-4866-99f8-5be71557142c
aws	gpu	1	16.00	\N	\N	1.018500	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 16:50:59+00	86334687-d63e-4275-bc51-eaf77e7dae7a
aws	gpu	A10G	24.00	\N	\N	3.010100	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 16:50:59+00	02dbd86d-0bd3-4631-b97d-f05284454353
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 16:50:59+00	762e2d7a-e075-407f-8ff8-a43df7872126
aws	gpu	T4	16.00	\N	\N	1.481000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 16:50:59+00	5f5395b7-a8e1-4ea8-b288-bd2526b2c8ad
aws	gpu	1	16.00	\N	\N	0.683900	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 16:50:59+00	a92a9eb0-1fcf-4267-82fe-4d34200f7939
aws	gpu	1	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 16:50:59+00	92f03229-8fdd-48ed-8e1b-2045244764ec
aws	gpu	1	16.00	\N	\N	0.683900	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 16:50:59+00	1b8f3eea-def2-4f07-b62a-ba56bf46331f
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 16:50:59+00	f760f478-0a18-44e1-99d8-1d2989152464
aws	gpu	T4	16.00	\N	\N	0.647000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 16:50:59+00	c9738fa3-6978-4078-bfbf-ea6fbc01ad2c
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 16:50:59+00	bb112331-d94e-438d-a394-f56ff30a01a2
aws	gpu	T4	16.00	\N	\N	5.353000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 16:50:59+00	f5875ea0-fc22-4755-b334-8c42a945dad4
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 16:50:59+00	0cd9d3f6-897d-4b17-902b-a136e702995c
aws	gpu	A10G	24.00	\N	\N	1.743600	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 16:50:59+00	857a7209-ff36-439c-b9ff-9ba7b86898ef
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 16:50:59+00	b4f7e8da-f3ff-46a0-92c2-cacd6bfbe5e2
aws	gpu	1	16.00	\N	\N	1.018500	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 16:50:59+00	c171ab2c-bc5a-470f-8899-be8d1c749cdc
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 16:50:59+00	b312468c-ad8e-4e18-a005-b9f3887c7ef1
aws	gpu	T4	16.00	\N	\N	2.677000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 16:50:59+00	88c5672f-8248-4572-806f-55d555492158
aws	gpu	T4	16.00	\N	\N	1.481000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 16:50:59+00	9d1b2c2e-4312-486e-a24f-e4d09cff54d9
aws	gpu	T4	16.00	\N	\N	5.353000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 16:50:59+00	abd6229f-359b-4c85-8ff3-b4cb826ca97d
aws	gpu	A10G	24.00	\N	\N	5.036500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 16:50:59+00	94f5f075-3e20-4022-89fb-bee58e8a974a
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 16:50:59+00	cb7b59b1-a98e-4043-9cdf-239ea14469e5
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 16:50:59+00	305e1ad4-f971-4e0d-82b1-12e67286f0c4
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 16:50:59+00	93f215ee-a739-49f6-9149-46e5eb785c9f
aws	gpu	T4	16.00	\N	\N	0.925000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 16:50:59+00	829fa980-4922-47e6-a55e-2806be119faf
aws	gpu	A100	40.00	\N	\N	3.801300	available	https://aws.amazon.com/ec2/instance-types/p4d/	128.00	400.00	2026-07-22 16:50:59+00	a608dd85-3f71-4a32-9cff-e24687d3538a
aws	gpu	A10G	24.00	\N	\N	1.743600	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 16:50:59+00	ac81af34-7e7c-4a00-95ab-4e0ae35faef9
aws	gpu	1	16.00	\N	\N	0.516600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 16:50:59+00	da6244f8-b62d-4b5d-89e8-dadba70fac4c
aws	gpu	A10G	24.00	\N	\N	1.490300	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 16:50:59+00	b89ba4ba-9751-405b-b637-f0610867c455
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 16:50:59+00	5b0a6f84-eac1-437b-9475-e23dacc3c21d
aws	gpu	A10G	24.00	\N	\N	1.237000	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 16:50:59+00	1a9b0c49-324b-4737-84f0-d00164ef2fdc
aws	gpu	1	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 16:50:59+00	aec94b53-d515-4f4d-ad73-3179d61b35ae
aws	gpu	T4	16.00	\N	\N	2.677000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 16:50:59+00	fdae1d7a-da14-4cc7-9810-b0c86eece73c
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 16:50:59+00	5891ea04-9d6e-408f-b892-282b8672b0f3
aws	gpu	A100	40.00	\N	\N	3.801300	available	https://aws.amazon.com/ec2/instance-types/p4d/	128.00	400.00	2026-07-22 16:50:59+00	8370b879-8b44-44f3-ac58-15cb4cfc9de9
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 16:50:59+00	1a212408-2475-4b6c-be8c-e473cfc32a0f
aws	gpu	1	16.00	\N	\N	0.516600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 16:50:59+00	7a119444-d935-42ee-b9f7-63df3125da45
aws	gpu	INFERENTIA2	32.00	\N	\N	0.909800	available	https://aws.amazon.com/ec2/instance-types/inf2/	32.00	250.00	2026-07-22 16:50:59+00	58fbd4d3-7e0a-4be7-9641-a38a22f71ce9
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 16:50:59+00	8db4222e-0579-466b-b6ac-152fdabf66ff
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 16:50:59+00	522a8e20-049b-492e-8c56-59b106dbce0b
aws	gpu	A10G	24.00	\N	\N	1.490300	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 16:50:59+00	86132509-9d68-4f96-a3a8-683a37d2b619
aws	gpu	T4	16.00	\N	\N	0.647000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 16:50:59+00	0c3bb72f-20a1-48c0-8d37-f999391fbd58
aws	gpu	INFERENTIA2	32.00	\N	\N	0.909800	available	https://aws.amazon.com/ec2/instance-types/inf2/	32.00	250.00	2026-07-22 16:50:59+00	4764c60c-5ddb-492f-a658-8ab29e0fbc3e
aws	gpu	A10G	24.00	\N	\N	1.996900	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 16:50:59+00	27080c12-8488-4e8c-81b5-3caf1901d8a4
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 16:50:59+00	72a16edd-e33b-4136-8077-2db9558fdd2f
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 16:50:59+00	a4f06db2-3dc2-4191-a3bd-0fa121c816f5
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 16:50:59+00	7569698a-0f12-43d0-ab22-14b453931b37
aws	gpu	A10G	24.00	\N	\N	5.036500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 16:50:59+00	24dd9c55-4420-4d44-8d4b-f5235fc5379c
aws	gpu	A10G	24.00	\N	\N	1.237000	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 16:50:59+00	2c875789-5e0a-48ed-83dc-d6e24d89c005
aws	gpu	T4	16.00	\N	\N	0.925000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 17:52:57+00	2c3222a9-2a86-4851-887c-b33ad1c6e1b9
aws	gpu	A10G	24.00	\N	\N	1.996900	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 17:52:57+00	cd7438fb-9b85-4d11-86c7-1687393e415a
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 17:52:57+00	5d499bfd-79ad-4288-b4dc-c452e6ce06ac
aws	gpu	A10G	24.00	\N	\N	3.010100	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 17:52:57+00	0243436e-8692-4910-8b2b-5e7c6d72e610
aws	gpu	1	16.00	\N	\N	1.018500	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 17:52:57+00	5fa7927e-46ed-47a8-924e-f566cc9af24a
aws	gpu	A10G	24.00	\N	\N	3.010100	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 17:52:57+00	9932a493-0bdd-4fd9-97c7-d02653e8f5ac
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 17:52:57+00	44eaa67b-9079-4043-852d-4748fbc8be2c
aws	gpu	T4	16.00	\N	\N	1.481000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 17:52:57+00	89ee70c6-a889-4f7d-9993-28b12f2917af
aws	gpu	1	16.00	\N	\N	0.683900	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 17:52:57+00	8a8747ca-50a0-47e1-8798-06c08a064e47
aws	gpu	1	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 17:52:57+00	816a2fc4-fba8-48a6-b84b-a60ea24a699f
aws	gpu	1	16.00	\N	\N	0.683900	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 17:52:57+00	fe134f08-1e39-433a-b18a-a134bf4fc570
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 17:52:57+00	fe5bee9a-a9be-422a-8620-8f50f1b85d2c
aws	gpu	T4	16.00	\N	\N	0.647000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 17:52:57+00	d9643b70-687e-4bd9-9fab-84addacafa27
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 17:52:57+00	38b95046-6138-4f42-bdf0-3cf2aa4f18cc
aws	gpu	T4	16.00	\N	\N	5.353000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 17:52:57+00	f9dcd6f8-31a5-4f69-8fc7-fc46f79ab6e6
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 17:52:57+00	2ef6471e-8cc8-4a03-92b6-03bd2d47f83b
aws	gpu	A10G	24.00	\N	\N	1.743600	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 17:52:57+00	570485b5-a6f2-4905-9a09-c077a281d048
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 17:52:57+00	22193714-8688-48b7-ab2b-25ad23ca4b42
aws	gpu	1	16.00	\N	\N	1.018500	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 17:52:57+00	4ec16bf8-c64d-4cba-bd2f-00e1911e7f7c
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 17:52:57+00	37f0097a-7642-49d7-9679-783f2c3e0b95
aws	gpu	T4	16.00	\N	\N	2.677000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 17:52:57+00	21cd6c84-34d7-4ced-b15b-3c4f75c38144
aws	gpu	T4	16.00	\N	\N	1.481000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 17:52:57+00	ce2c3c11-5102-4d41-b30a-35f359964e1f
aws	gpu	T4	16.00	\N	\N	5.353000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 17:52:57+00	731dc7d4-e899-4a23-9840-e0d59862c3b8
aws	gpu	A10G	24.00	\N	\N	5.036500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 17:52:57+00	b548bf63-6dca-4ab7-aac9-f9e0482fb290
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 17:52:57+00	0ee114ac-fad9-4dd4-baec-f805681382ef
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 17:52:57+00	37405d75-26c4-451f-9ee2-6c5b40596856
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 17:52:57+00	a30d1fb1-5f4b-4966-b795-e9c32e4f0b9e
aws	gpu	T4	16.00	\N	\N	0.925000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 17:52:57+00	d4d00149-dd7d-4af4-84fe-0739dac18352
aws	gpu	A100	40.00	\N	\N	3.801300	available	https://aws.amazon.com/ec2/instance-types/p4d/	128.00	400.00	2026-07-22 17:52:57+00	474f29cc-b8f3-4c6d-b4d5-6b6dee48b04f
aws	gpu	A10G	24.00	\N	\N	1.743600	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 17:52:57+00	66a26ab7-4d33-420d-bc64-aaf3df73b019
aws	gpu	1	16.00	\N	\N	0.516600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 17:52:57+00	329be02c-c4ec-442a-8c44-ddd177e1416f
aws	gpu	A10G	24.00	\N	\N	1.490300	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 17:52:57+00	d8d59839-dcaf-42cd-a510-e03d1302f800
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 17:52:57+00	332af929-f1cf-43cb-a270-dd98772ceaaa
aws	gpu	A10G	24.00	\N	\N	1.237000	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 17:52:57+00	6e0be456-ce1f-41ca-b7b0-3bd3177375d7
aws	gpu	1	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 17:52:57+00	4b981fc3-8289-40c5-8608-584907131795
aws	gpu	T4	16.00	\N	\N	2.677000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 17:52:57+00	23be57ed-33a3-4561-b36c-601352899005
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 17:52:57+00	58c7c911-4e55-4b24-9b3c-efb57583cebb
aws	gpu	A100	40.00	\N	\N	3.801300	available	https://aws.amazon.com/ec2/instance-types/p4d/	128.00	400.00	2026-07-22 17:52:57+00	802620d0-3141-4b89-9abc-7f40ed1784dc
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 17:52:57+00	8e7b7d8f-ceb3-4508-b00d-21d4e514e3ca
aws	gpu	1	16.00	\N	\N	0.516600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 17:52:57+00	49dcfe28-10b6-4268-b194-4d13d1996bd0
aws	gpu	INFERENTIA2	32.00	\N	\N	0.909800	available	https://aws.amazon.com/ec2/instance-types/inf2/	32.00	250.00	2026-07-22 17:52:57+00	1ca09f5b-74a9-43b0-afff-d8b06f0a8d1b
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 17:52:57+00	9c94436d-1300-4348-98a8-1ab167ec50ed
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 17:52:57+00	ad2cbf3f-0c16-4c56-a508-5503cde4bd70
aws	gpu	A10G	24.00	\N	\N	1.490300	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 17:52:57+00	26d01513-76e1-443e-accf-2d26831c06c7
aws	gpu	T4	16.00	\N	\N	0.647000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 17:52:57+00	7b289454-6fea-49ee-9f2b-27ea75f71aa2
aws	gpu	INFERENTIA2	32.00	\N	\N	0.909800	available	https://aws.amazon.com/ec2/instance-types/inf2/	32.00	250.00	2026-07-22 17:52:57+00	fa100cec-ccad-46ce-84f5-8eb284e7e7d4
aws	gpu	A10G	24.00	\N	\N	1.996900	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 17:52:57+00	779e4e39-7a89-4056-9ca0-fe3cd79cc15a
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 17:52:57+00	08c2db9c-8869-4c3b-882e-68616aeab481
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 17:52:57+00	a4ac8025-4e3f-4d86-902b-ee05b2b88d41
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 17:52:57+00	2c0f97ab-cd94-4d74-aa5a-840e2acdade3
aws	gpu	A10G	24.00	\N	\N	5.036500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 17:52:57+00	2c11c5d8-e061-4467-a486-eea05466c859
aws	gpu	A10G	24.00	\N	\N	1.237000	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 17:52:57+00	eeca31c1-f485-4a77-84d1-71b3e78bc014
aws	gpu	T4	16.00	\N	\N	0.925000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 18:00:46+00	586abe11-193a-4faa-9fca-65038cbc1e37
aws	gpu	A10G	24.00	\N	\N	1.996900	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 18:00:46+00	5c528673-0c5b-4f53-84c4-830b8eb45246
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 18:00:46+00	4a6a0aca-9aad-4bf7-9707-7af80fecbdd1
aws	gpu	A10G	24.00	\N	\N	3.010100	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 18:00:46+00	64482870-7b3e-4d21-b6e4-1d32d5ea9fd8
aws	gpu	1	16.00	\N	\N	1.018500	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 18:00:46+00	46225f48-b7ca-41b0-b916-b0e776704c8d
aws	gpu	A10G	24.00	\N	\N	3.010100	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 18:00:46+00	75421c47-aa5b-4039-8559-1bd227ddc3d0
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 18:00:46+00	76ea12c9-656f-48b9-bb08-5eb084a78421
aws	gpu	T4	16.00	\N	\N	1.481000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 18:00:46+00	62dcd6a1-bbd3-47fa-b76e-39b88aa9f5e5
aws	gpu	1	16.00	\N	\N	0.683900	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 18:00:46+00	0801be33-892a-4e13-a4fa-84a99e563aca
aws	gpu	1	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 18:00:46+00	ff2fb1d2-c726-4d4d-8691-ff9900d05e58
aws	gpu	1	16.00	\N	\N	0.683900	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 18:00:46+00	d4f2f351-314d-498e-be2a-ff03b9e437ce
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 18:00:46+00	3545775f-13d3-41a3-a9cb-c38b3c87da77
aws	gpu	T4	16.00	\N	\N	0.647000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 18:00:46+00	07771a52-4554-417e-beb3-3536a1e475c3
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 18:00:46+00	13a915b6-b71f-4dd6-90fa-014b11db8f36
aws	gpu	T4	16.00	\N	\N	5.353000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 18:00:46+00	c6aa6ff2-771e-4f8b-9a71-42c51add6440
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 18:00:46+00	4c17526a-8c52-4e59-b1ef-88b8f803aff7
aws	gpu	A10G	24.00	\N	\N	1.743600	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 18:00:46+00	b52e7ceb-dfa8-4983-999f-dbdb8acc2e67
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 18:00:46+00	34a8d35a-f1cc-437c-880f-4b51f502db38
aws	gpu	1	16.00	\N	\N	1.018500	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 18:00:46+00	cd61530f-6ca1-46ef-b2af-4a6aaf005f9a
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 18:00:46+00	029848ac-070a-45ea-9a1f-4dfc42843bc8
aws	gpu	T4	16.00	\N	\N	2.677000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 18:00:46+00	23f8accc-bf65-4a8c-972f-3681d516650d
aws	gpu	T4	16.00	\N	\N	1.481000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 18:00:46+00	6863a056-ffc5-4052-a4d5-59a0d8852cdc
aws	gpu	T4	16.00	\N	\N	5.353000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 18:00:46+00	9f8577aa-9b7d-43a3-812d-4b872d276848
aws	gpu	A10G	24.00	\N	\N	5.036500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 18:00:46+00	0e55450d-36f0-4c61-bc53-16ef44aefc49
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 18:00:46+00	7ae3548e-3e07-4857-ae97-2c811085e0ed
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 18:00:46+00	0804aa8a-ef9d-48a6-8479-5b28a9150236
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 18:00:46+00	e8931333-88f7-472d-8500-2af9bb5622d4
aws	gpu	T4	16.00	\N	\N	0.925000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 18:00:46+00	56a99d41-be04-4f4e-993e-88d4c8be2ae3
aws	gpu	A100	40.00	\N	\N	3.801300	available	https://aws.amazon.com/ec2/instance-types/p4d/	128.00	400.00	2026-07-22 18:00:46+00	f417bbbb-ee52-458c-a73e-31b2757c85c2
aws	gpu	A10G	24.00	\N	\N	1.743600	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 18:00:46+00	475071ae-0560-4785-a8d5-17fb9b868211
aws	gpu	1	16.00	\N	\N	0.516600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 18:00:46+00	bb0b5f1b-3696-4f3f-8289-a8b7379169ee
aws	gpu	A10G	24.00	\N	\N	1.490300	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 18:00:46+00	f680ee92-5a24-4d35-9d3c-b19523f922aa
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 18:00:46+00	10eef26a-56d1-4e08-834e-67c06a8ba272
aws	gpu	A10G	24.00	\N	\N	1.237000	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 18:00:46+00	2a670fa1-34d7-4a13-b801-16693a14efc7
aws	gpu	1	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 18:00:46+00	1247ad27-60a4-4911-998a-06b926822fc4
aws	gpu	T4	16.00	\N	\N	2.677000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 18:00:46+00	d88adf06-34e4-498b-a36c-ce80b055481a
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 18:00:46+00	bee43823-197a-49be-b622-d81aab4eed8e
aws	gpu	A100	40.00	\N	\N	3.801300	available	https://aws.amazon.com/ec2/instance-types/p4d/	128.00	400.00	2026-07-22 18:00:46+00	3945a2e6-2919-427a-9154-fad08e5b6c13
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 18:00:46+00	62f14d3c-aa0b-4566-bb2d-137426690219
aws	gpu	1	16.00	\N	\N	0.516600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 18:00:46+00	c493a5e4-92b9-4b9f-91b0-4ccd70f42a9c
aws	gpu	INFERENTIA2	32.00	\N	\N	0.909800	available	https://aws.amazon.com/ec2/instance-types/inf2/	32.00	250.00	2026-07-22 18:00:46+00	8e5f0f49-7717-49e9-a9bb-b30417a80e44
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 18:00:46+00	7475613c-409e-45d1-8b36-1825262645dd
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 18:00:46+00	17f09135-f5be-42dc-a34f-7dd7d49de37a
aws	gpu	A10G	24.00	\N	\N	1.490300	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 18:00:46+00	ed5def03-9485-4f85-acc1-81204644f9a0
aws	gpu	T4	16.00	\N	\N	0.647000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 18:00:46+00	587db3de-eeb2-45cd-84f2-59880c303936
aws	gpu	INFERENTIA2	32.00	\N	\N	0.909800	available	https://aws.amazon.com/ec2/instance-types/inf2/	32.00	250.00	2026-07-22 18:00:46+00	ae4d82e4-0ee9-4fe7-b0a7-d8b4aeff5bac
aws	gpu	A10G	24.00	\N	\N	1.996900	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 18:00:46+00	359595a5-8323-4907-9710-337e0215d93b
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 18:00:46+00	f4dac7cb-57c2-49d4-88cf-084f18ddf8dd
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 18:00:46+00	6482b7d7-61fd-489e-926f-96d544912868
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 18:00:46+00	109fb76c-1640-4292-83e2-d4ac6c76beb1
aws	gpu	A10G	24.00	\N	\N	5.036500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 18:00:46+00	4aee2c42-0835-40fb-8f8b-62b2610ae4d2
aws	gpu	A10G	24.00	\N	\N	1.237000	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 18:00:46+00	b6ffaab8-ce55-4b55-bb72-b15d828e34ff
aws	gpu	T4	16.00	\N	\N	0.925000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 18:01:10+00	2c2ada45-9654-455f-98d5-a4971db43ebd
aws	gpu	A10G	24.00	\N	\N	1.996900	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 18:01:10+00	3220fa2d-ad5e-43e3-a180-ebda0a45d75e
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 18:01:10+00	62ddfbdb-ac3a-4410-af04-e64052e12918
aws	gpu	A10G	24.00	\N	\N	3.010100	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 18:01:10+00	9e3b423a-e385-43de-90e5-1af85e9794b5
aws	gpu	1	16.00	\N	\N	1.018500	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 18:01:10+00	5a0d5e1f-9062-4576-97e7-5b1272af84de
aws	gpu	A10G	24.00	\N	\N	3.010100	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 18:01:10+00	8f80438f-367f-4408-a823-a7d489f12124
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 18:01:10+00	7fa1feb1-a01e-4915-882c-a2ddd73fe289
aws	gpu	T4	16.00	\N	\N	1.481000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 18:01:10+00	1ff201ed-ef15-43ad-9ffa-d14fd88fb9b3
aws	gpu	1	16.00	\N	\N	0.683900	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 18:01:10+00	5a5e947f-81a8-461a-ad90-df604c830a58
aws	gpu	1	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 18:01:10+00	b1cd352c-c955-4bdd-8035-dc5f512f66e3
aws	gpu	1	16.00	\N	\N	0.683900	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 18:01:10+00	7d828606-dca7-4b1a-a7a3-62f812e5e101
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 18:01:10+00	fc44b1f9-6bc5-4275-a76b-708058732c67
aws	gpu	T4	16.00	\N	\N	0.647000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 18:01:10+00	1a501395-545f-4de2-aae0-dff526eb0116
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 18:01:10+00	c49d4c3c-f0a7-49e6-b5dc-6bf32dcddb85
aws	gpu	T4	16.00	\N	\N	5.353000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 18:01:10+00	249bea75-3046-49a8-93d5-72e34899cc80
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 18:01:10+00	5b077a3b-fe14-47f9-9a5a-f3dd3d06bccf
aws	gpu	A10G	24.00	\N	\N	1.743600	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 18:01:10+00	91bb6dd8-bb8c-4172-8736-cea5a5e190cc
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 18:01:10+00	2299e954-9de6-4a6b-af15-2451e10492aa
aws	gpu	1	16.00	\N	\N	1.018500	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 18:01:10+00	d8c0f711-40a2-4da5-ac3f-9366065080e1
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 18:01:10+00	2b68372f-61d4-46ad-8fbe-013449d8acf5
aws	gpu	T4	16.00	\N	\N	2.677000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 18:01:10+00	3116ae18-a9d3-4df0-a193-c911f94b62bc
aws	gpu	T4	16.00	\N	\N	1.481000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 18:01:10+00	b5c3500e-3779-4d8c-bad4-196c184af29c
aws	gpu	T4	16.00	\N	\N	5.353000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 18:01:10+00	81572e7a-9ebc-4920-b27f-6046dad80a8a
aws	gpu	A10G	24.00	\N	\N	5.036500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 18:01:10+00	614aec68-6ee1-4a6c-adf1-d887bab8ccf6
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 18:01:10+00	3c37531c-9972-42a5-83cc-2e8d25726b1a
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 18:01:10+00	adb44142-9601-4cb8-baf8-0049c493cac5
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 18:01:10+00	c9e46682-9c87-4aa6-8b3c-34d9ccbeab88
aws	gpu	T4	16.00	\N	\N	0.925000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 18:01:10+00	62c51146-565f-4c65-bff7-e73a2386d018
aws	gpu	A100	40.00	\N	\N	3.801300	available	https://aws.amazon.com/ec2/instance-types/p4d/	128.00	400.00	2026-07-22 18:01:10+00	677c99d9-f297-42ef-a84e-e515544b93e6
aws	gpu	A10G	24.00	\N	\N	1.743600	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 18:01:10+00	71851a00-47c5-4070-a57d-a622ae313041
aws	gpu	1	16.00	\N	\N	0.516600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 18:01:10+00	001d49ff-f1a0-4842-a4bd-307ea43cdf65
aws	gpu	A10G	24.00	\N	\N	1.490300	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 18:01:10+00	adac458c-3925-4879-9c91-7b605b8345cc
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 18:01:10+00	2f493a32-815d-4738-8c80-d90c20c818d5
aws	gpu	A10G	24.00	\N	\N	1.237000	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 18:01:10+00	517af343-1f47-47c1-a7a6-20cb1946aa13
aws	gpu	1	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 18:01:10+00	7362f9b2-a702-45d7-a413-74340015251f
aws	gpu	T4	16.00	\N	\N	2.677000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 18:01:10+00	f11bd39b-7a3b-43a9-9b44-ebe7c76feacb
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 18:01:10+00	610254cb-f6d1-4a00-b63a-70191bbc2ca8
aws	gpu	A100	40.00	\N	\N	3.801300	available	https://aws.amazon.com/ec2/instance-types/p4d/	128.00	400.00	2026-07-22 18:01:10+00	d6791179-b007-47a2-b2ad-669ad8249b19
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 18:01:10+00	19766ea9-89d1-4e76-8b90-16c1452e4683
aws	gpu	1	16.00	\N	\N	0.516600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 18:01:10+00	d673eafe-39b5-4e24-9548-8a3a7cae2093
aws	gpu	INFERENTIA2	32.00	\N	\N	0.909800	available	https://aws.amazon.com/ec2/instance-types/inf2/	32.00	250.00	2026-07-22 18:01:10+00	a801f036-a66c-4ed9-aacf-1ddf09677ee4
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 18:01:10+00	d450b322-8782-4d27-a4f4-b1489e31a284
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 18:01:10+00	d25a9e36-1c3c-4016-8e4b-321c89d1723c
aws	gpu	A10G	24.00	\N	\N	1.490300	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 18:01:10+00	283f0725-c549-4846-9676-66bf916f7415
aws	gpu	T4	16.00	\N	\N	0.647000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 18:01:10+00	dfa444fb-bd43-4f51-a207-9921bbefef3e
aws	gpu	INFERENTIA2	32.00	\N	\N	0.909800	available	https://aws.amazon.com/ec2/instance-types/inf2/	32.00	250.00	2026-07-22 18:01:10+00	def0d4a2-5944-49bb-ad6b-2ada8eda1702
aws	gpu	A10G	24.00	\N	\N	1.996900	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 18:01:10+00	c191646b-72bb-4b89-b164-d143380a8401
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 18:01:10+00	0ab3714e-24af-4339-a1e6-f12bf4df9b23
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 18:01:10+00	f56ac653-3f80-4d57-ac76-8cb00c17d799
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 18:01:10+00	4025c3d6-ad75-47e6-b5eb-84d0fd8e0565
aws	gpu	A10G	24.00	\N	\N	5.036500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 18:01:10+00	1fe25f84-f10a-4a11-8faa-b801d3f4ca8a
aws	gpu	A10G	24.00	\N	\N	1.237000	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 18:01:10+00	2f696e7a-49e0-4cf6-820f-284c4cfee451
aws	gpu	T4	16.00	\N	\N	0.925000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:09:22+00	2ea9e3f5-2fb3-4703-9979-1b67c7d5b2b6
aws	gpu	A10G	24.00	\N	\N	1.996900	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:09:22+00	d5ecbe42-7691-4daa-a53c-f32b3469980a
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 19:09:22+00	6597741c-73b9-4034-8eed-e89295d250a7
aws	gpu	A10G	24.00	\N	\N	3.010100	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:09:22+00	9e389339-8764-4a3d-90f3-8f1d4fce1d3c
aws	gpu	1	16.00	\N	\N	1.018500	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:09:22+00	78c329b6-6f34-4c2e-a6fd-66aa9d19d7bb
aws	gpu	A10G	24.00	\N	\N	3.010100	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:09:22+00	add54416-1562-4c3a-b9d0-8bfa0583cf40
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 19:09:22+00	b50ac259-415c-4864-8246-57279efa6f1d
aws	gpu	T4	16.00	\N	\N	1.481000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:09:22+00	92379f5f-b597-4fd7-8669-b22cbc79542a
aws	gpu	1	16.00	\N	\N	0.683900	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:09:22+00	51959985-803f-4eee-9a8d-031b487aa17c
aws	gpu	1	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:09:22+00	dabb79c6-ffc3-4991-9b15-295d82af4498
aws	gpu	1	16.00	\N	\N	0.683900	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:09:22+00	c732d2bd-8deb-4a07-9408-47e5d86672d7
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:09:22+00	59164b06-33e0-4ad3-9f8e-4c896657ac81
aws	gpu	T4	16.00	\N	\N	0.647000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:09:22+00	fb5d6d45-a8e6-4e50-bead-4a63f12dbae8
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:09:22+00	c48d3a59-7e42-4a97-ad20-85d9493f97f5
aws	gpu	T4	16.00	\N	\N	5.353000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:09:22+00	5d9cbe75-34a8-420d-8123-1584a3626fd5
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:09:22+00	41c0feaa-9d40-4f6d-94ef-a626d61ca398
aws	gpu	A10G	24.00	\N	\N	1.743600	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:09:22+00	181d7a68-c8cb-4692-94a9-cd7921fac8c7
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:09:22+00	b074850c-2c32-434d-9723-a883465f46cf
aws	gpu	1	16.00	\N	\N	1.018500	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:09:22+00	92630f0e-ae2e-4654-a8a7-f137b62f5c14
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 19:09:22+00	256f0b0d-3f24-4f55-9efc-2e58d5683f33
aws	gpu	T4	16.00	\N	\N	2.677000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:09:22+00	85a8f714-5a6b-43d4-9507-f7122ae5aebc
aws	gpu	T4	16.00	\N	\N	1.481000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:09:22+00	a811351b-235c-445c-aeaf-f0f3a89cc006
aws	gpu	T4	16.00	\N	\N	5.353000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:09:22+00	ff637a92-d39f-458f-a6f2-f706609353f9
aws	gpu	A10G	24.00	\N	\N	5.036500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:09:22+00	b2353a41-9366-4639-a6ec-54fbc8b6b9a2
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 19:09:22+00	89b3e888-37f2-4687-9e5b-6a72bbba54b2
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:09:22+00	9e7f800a-2e12-440f-b6ec-e5bcd4af585a
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:09:22+00	6ee20fcc-7861-476c-970a-1dc915e4fc1d
aws	gpu	T4	16.00	\N	\N	0.925000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:09:22+00	125d3753-1ac0-49d8-a154-1b499fd86590
aws	gpu	A100	40.00	\N	\N	3.801300	available	https://aws.amazon.com/ec2/instance-types/p4d/	128.00	400.00	2026-07-22 19:09:22+00	253beb33-3fc2-483e-bf06-216f50b7dd8b
aws	gpu	A10G	24.00	\N	\N	1.743600	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:09:22+00	980fd6fc-56ea-44f0-8f98-842b4dc08fc4
aws	gpu	1	16.00	\N	\N	0.516600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:09:22+00	b12d8534-ff50-48a5-9d20-6a29ec4b0162
aws	gpu	A10G	24.00	\N	\N	1.490300	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:09:22+00	7263ded4-d3b7-4f41-afb8-e99f13d303a2
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 19:09:22+00	f654c50e-9845-4457-b4b3-64bf2ef14b4c
aws	gpu	A10G	24.00	\N	\N	1.237000	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:09:22+00	ca7c3d13-9856-4a85-8359-755b82d04b67
aws	gpu	1	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:09:22+00	c6807b05-0ff9-4c54-b1c4-5813f2afbe94
aws	gpu	T4	16.00	\N	\N	2.677000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:09:22+00	32decbdf-c038-4d0a-9f6e-931d7e6ccfc5
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:09:22+00	339b0a9b-dbfa-40e1-a5a4-b8014743c74a
aws	gpu	A100	40.00	\N	\N	3.801300	available	https://aws.amazon.com/ec2/instance-types/p4d/	128.00	400.00	2026-07-22 19:09:22+00	f5110a6e-1d5a-47ca-a06b-a03c0a0ea48b
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:09:22+00	4b2ef4cf-3d5c-4c0f-884e-ee37db2fddc2
aws	gpu	1	16.00	\N	\N	0.516600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:09:22+00	b6c67897-577a-4ac3-8894-777a71c58257
aws	gpu	INFERENTIA2	32.00	\N	\N	0.909800	available	https://aws.amazon.com/ec2/instance-types/inf2/	32.00	250.00	2026-07-22 19:09:22+00	701f0e99-9037-4d6b-884c-b1c2dcce64f7
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 19:09:22+00	acfbacd6-c48d-455a-83e0-e05b61474e42
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:09:22+00	3de63d77-cfde-4c8c-9729-ef69c1402596
aws	gpu	A10G	24.00	\N	\N	1.490300	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:09:22+00	208832ba-a317-48d2-9dfc-fd1bd1bff7d7
aws	gpu	T4	16.00	\N	\N	0.647000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:09:22+00	6168c53e-419a-49c2-8d2e-4744956388e3
aws	gpu	INFERENTIA2	32.00	\N	\N	0.909800	available	https://aws.amazon.com/ec2/instance-types/inf2/	32.00	250.00	2026-07-22 19:09:22+00	dfbdb869-31d0-442b-b7ca-3a64758acb83
aws	gpu	A10G	24.00	\N	\N	1.996900	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:09:22+00	14749d7c-e889-4322-ac9c-486e5bd596e8
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:09:22+00	40220c45-5b30-4551-9643-7cc589608763
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:09:22+00	adcbe388-ced5-4df1-b35d-00358ec563ab
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:09:22+00	d68a5737-cba9-4516-9fe5-6b26f3fa2b2f
aws	gpu	A10G	24.00	\N	\N	5.036500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:09:22+00	cfefda67-8439-4e4e-bcf3-ca09fd563b59
aws	gpu	A10G	24.00	\N	\N	1.237000	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:09:22+00	52c2d50b-88c9-4461-ae96-9c49610093e4
aws	gpu	T4	16.00	\N	\N	0.925000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:19:15+00	52edec47-d261-4a7c-a9d5-f91b80dbade0
aws	gpu	A10G	24.00	\N	\N	1.996900	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:19:15+00	552a92e7-495e-44bc-a03b-a9b5810e1030
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 19:19:15+00	e2dd9955-d84a-4ae0-9a60-a4ea08cb1636
aws	gpu	A10G	24.00	\N	\N	3.010100	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:19:15+00	be0a554d-4cd2-43cb-ae99-16c59682a686
aws	gpu	1	16.00	\N	\N	1.018500	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:19:15+00	0f0d6d66-423c-4434-bf69-672b2715a44a
aws	gpu	A10G	24.00	\N	\N	3.010100	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:19:15+00	1c97056a-d454-4baa-9dc0-61615340e786
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 19:19:15+00	667a14a6-b842-432f-8aaa-cdfa24e5caca
aws	gpu	T4	16.00	\N	\N	1.481000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:19:15+00	cbecd0fa-0b5f-4bb8-b555-c10f77101f94
aws	gpu	1	16.00	\N	\N	0.683900	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:19:15+00	5a7b397c-d798-4d06-bb6f-497b624a58ec
aws	gpu	1	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:19:15+00	25750abf-4a86-46dd-ae03-1f6521503427
aws	gpu	1	16.00	\N	\N	0.683900	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:19:15+00	8f840bfe-4a57-4126-ac05-384fc418ba6f
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:19:15+00	4d0f6cef-9c5c-4189-b5d8-aeab4cb67127
aws	gpu	T4	16.00	\N	\N	0.647000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:19:15+00	701e7501-b4c2-4748-a4b3-7ff32e7eb125
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:19:15+00	6bd02a5d-6264-45d1-8e1a-f129030ffea9
aws	gpu	T4	16.00	\N	\N	5.353000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:19:15+00	0674ae83-7ef0-419a-ab51-8e7f7e0e282b
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:19:15+00	93020598-6ecc-4cc8-bbbb-945425f5cd67
aws	gpu	A10G	24.00	\N	\N	1.743600	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:19:15+00	1e50072b-5394-4162-b8fa-060ef06238ca
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:19:15+00	41b0a46f-addc-42e1-9f6e-3349ed310832
aws	gpu	1	16.00	\N	\N	1.018500	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:19:15+00	d8544604-055c-4412-b960-d5a2ca25a13f
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 19:19:15+00	31456e1d-2ab6-4418-9c75-016d5440341c
aws	gpu	T4	16.00	\N	\N	2.677000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:19:15+00	19ca3047-22db-4ae6-aa8e-23b62d766ea4
aws	gpu	T4	16.00	\N	\N	1.481000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:19:15+00	1fc2b6e3-4367-4d57-bb13-a319c457860a
aws	gpu	T4	16.00	\N	\N	5.353000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:19:15+00	e9e476d1-832e-4286-9e76-c507012ec7ef
aws	gpu	A10G	24.00	\N	\N	5.036500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:19:15+00	97632b99-e3df-42e1-a48f-2faf3bc0002b
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 19:19:15+00	7e19d83f-e3cd-4a93-947c-321cac09fee0
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:19:15+00	e99de9e6-f45b-48ab-9ded-2e8cb0218e32
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:19:15+00	f9333de6-021d-4b33-81fb-0f0a3a7ceb70
aws	gpu	T4	16.00	\N	\N	0.925000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:19:15+00	a6b8ea02-8818-4b0f-9e84-e90b769e7023
aws	gpu	A100	40.00	\N	\N	3.801300	available	https://aws.amazon.com/ec2/instance-types/p4d/	128.00	400.00	2026-07-22 19:19:15+00	a851ccab-223d-4218-88ab-5dcdc588bbc0
aws	gpu	A10G	24.00	\N	\N	1.743600	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:19:15+00	bbb574f0-fd30-4435-bed0-aa56f1887f72
aws	gpu	1	16.00	\N	\N	0.516600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:19:15+00	e3b823f2-d51c-41ab-bd1a-2b48019a4273
aws	gpu	A10G	24.00	\N	\N	1.490300	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:19:15+00	6ea51a9b-a33d-448f-8d13-c6a42b88b88f
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 19:19:15+00	2b1b6f74-4100-4ad0-820e-661df3a56b03
aws	gpu	A10G	24.00	\N	\N	1.237000	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:19:15+00	ff343071-55e0-412c-9916-c2d124611eee
aws	gpu	1	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:19:15+00	74d3126f-0cfc-4c60-bff5-144fce4f20a3
aws	gpu	T4	16.00	\N	\N	2.677000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:19:15+00	9b54f3a2-b4a0-4658-bb8e-fb373ad84252
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:19:15+00	05ed7442-d938-4333-a496-c3378241a5d2
aws	gpu	A100	40.00	\N	\N	3.801300	available	https://aws.amazon.com/ec2/instance-types/p4d/	128.00	400.00	2026-07-22 19:19:15+00	49e8b472-19cc-4fe5-873c-d4879725dfa1
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:19:15+00	0298fba8-1c45-42b9-8d97-7b914fc0b233
aws	gpu	1	16.00	\N	\N	0.516600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:19:15+00	f8c24283-f062-4aba-8b9e-edc8ae3d3ca6
aws	gpu	INFERENTIA2	32.00	\N	\N	0.909800	available	https://aws.amazon.com/ec2/instance-types/inf2/	32.00	250.00	2026-07-22 19:19:15+00	2a3c69e4-fd9c-43cc-9556-5fc2294f208c
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 19:19:15+00	8a08099e-8ba3-4e59-a444-a5f17856788b
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:19:15+00	642014da-33e5-41b8-ab7e-0d8acb6c1eeb
aws	gpu	A10G	24.00	\N	\N	1.490300	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:19:15+00	a0db5291-879e-4d8b-b39a-ce4877347271
aws	gpu	T4	16.00	\N	\N	0.647000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:19:15+00	6b7d2ee3-2ded-4339-b60e-b4e12cddab1c
aws	gpu	INFERENTIA2	32.00	\N	\N	0.909800	available	https://aws.amazon.com/ec2/instance-types/inf2/	32.00	250.00	2026-07-22 19:19:15+00	e08f1ced-2873-439c-8b2a-837702c2a1f2
aws	gpu	A10G	24.00	\N	\N	1.996900	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:19:15+00	11011c9d-865f-4e39-bba1-b089cb3bdaab
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:19:15+00	a98828e0-c53e-407d-9077-d7c5971bc68e
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:19:15+00	b95d60e7-58b5-4ef6-876a-b79fe50c365f
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:19:15+00	fa4706ff-6b1f-4744-9c1d-1b0db088dde5
aws	gpu	A10G	24.00	\N	\N	5.036500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:19:15+00	d9d2e2ad-b480-4ce9-95ea-29a8483a7228
aws	gpu	A10G	24.00	\N	\N	1.237000	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:19:15+00	532337c2-c3b5-4b4f-8b8d-0fe749a8e297
aws	gpu	T4	16.00	\N	\N	0.925000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:33:46+00	73d90a37-9305-492b-b075-bac248a257c2
aws	gpu	A10G	24.00	\N	\N	1.996900	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:33:46+00	47055f18-b55b-451c-ac64-73cf706aaead
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 19:33:46+00	51eeac70-0a8b-4acc-9d50-efe330339134
aws	gpu	A10G	24.00	\N	\N	3.010100	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:33:46+00	7c75adaa-517c-4ce7-a440-dd1cd1c79d05
aws	gpu	1	16.00	\N	\N	1.018500	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:33:46+00	da9c6ca3-5cc9-4f80-b834-6da01458dec1
aws	gpu	A10G	24.00	\N	\N	3.010100	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:33:46+00	732bfd63-5f85-465e-a617-21e155e46b95
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 19:33:46+00	82ccd416-93d9-4733-9f97-6e1699fbe0e3
aws	gpu	T4	16.00	\N	\N	1.481000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:33:46+00	cc59a1e3-49ee-4e92-a489-6f261f7d9a26
aws	gpu	1	16.00	\N	\N	0.683900	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:33:46+00	ac8fc211-ee27-4245-b9f0-50b699d71fa5
aws	gpu	1	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:33:46+00	e9687cb6-ce05-48ba-bfa1-953377e5fdac
aws	gpu	1	16.00	\N	\N	0.683900	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:33:46+00	c2bf1899-f360-4d9b-a498-3fd3a1f03367
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:33:46+00	3ae31a61-f0dc-4450-b6d7-5b869c99ea4a
aws	gpu	T4	16.00	\N	\N	0.647000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:33:46+00	7d27688e-b2e1-4bb8-9fe9-271e355652af
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:33:46+00	4c606808-d1b4-48fc-9b94-82649ba135df
aws	gpu	T4	16.00	\N	\N	5.353000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:33:46+00	e5a809c9-f6bd-4602-a67d-22ad379139cc
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:33:46+00	0d33e787-2989-41db-adce-ceb32bff57ff
aws	gpu	A10G	24.00	\N	\N	1.743600	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:33:46+00	752c5db6-3555-473b-8587-109acae8c988
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:33:46+00	fe132985-cb19-471d-8dea-53c4775f458d
aws	gpu	1	16.00	\N	\N	1.018500	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:33:46+00	df3d9e09-ffdf-47b3-8f24-9c183f82a773
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 19:33:46+00	b3d90dc3-b318-45c5-9a86-2e66d1d81332
aws	gpu	T4	16.00	\N	\N	2.677000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:33:46+00	c7c5d476-87c7-4166-b5ef-b267e2c02f26
aws	gpu	T4	16.00	\N	\N	1.481000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:33:46+00	3af8fa01-86e4-439b-bb4c-976736a7e97e
aws	gpu	T4	16.00	\N	\N	5.353000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:33:46+00	654257b9-fa4d-4db2-b13d-0302b6481709
aws	gpu	A10G	24.00	\N	\N	5.036500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:33:46+00	f1b45bd3-1ee1-4f63-9f4d-b09173f2c353
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 19:33:46+00	ff02687b-72dc-423d-9efd-4e1d28b04ed3
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:33:46+00	a5551c80-c3df-4410-9285-9987b552ecee
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:33:46+00	097f35f0-3a33-4a6b-a1ee-f8e2bb240a8f
aws	gpu	T4	16.00	\N	\N	0.925000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:33:46+00	5fbc76ac-d6b9-42ee-9301-b7a286a7fc97
aws	gpu	A100	40.00	\N	\N	3.801300	available	https://aws.amazon.com/ec2/instance-types/p4d/	128.00	400.00	2026-07-22 19:33:46+00	3331f465-9143-4450-aa88-7634d49b8545
aws	gpu	A10G	24.00	\N	\N	1.743600	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:33:46+00	ad3078bd-e2d6-4d83-9728-e28e8be1f0ad
aws	gpu	1	16.00	\N	\N	0.516600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:33:46+00	167287a1-8a61-4e66-bd7d-98a872fa07f1
aws	gpu	A10G	24.00	\N	\N	1.490300	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:33:46+00	048b9004-bb1d-4a6c-bf2d-4512b8806373
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 19:33:46+00	4e85e4e5-7459-44f2-bb0e-3dfc20e26b58
aws	gpu	A10G	24.00	\N	\N	1.237000	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:33:46+00	d2da89d0-5965-423f-a921-4db31dab915e
aws	gpu	1	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:33:46+00	06fcf0b8-8c8a-49a4-9c80-ea4ec1ee5fc5
aws	gpu	T4	16.00	\N	\N	2.677000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:33:46+00	1965fa36-1ca0-4914-9701-878ab90fb559
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:33:46+00	6cad5218-c2df-4a7e-9201-26da125ecbbc
aws	gpu	A100	40.00	\N	\N	3.801300	available	https://aws.amazon.com/ec2/instance-types/p4d/	128.00	400.00	2026-07-22 19:33:46+00	7274d6ba-e755-418d-8d09-dfbfa1f94093
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:33:46+00	2c056e98-24ea-4862-8865-c9105220199c
aws	gpu	1	16.00	\N	\N	0.516600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:33:46+00	675b0b15-99e6-4927-92f1-8018951f5881
aws	gpu	INFERENTIA2	32.00	\N	\N	0.909800	available	https://aws.amazon.com/ec2/instance-types/inf2/	32.00	250.00	2026-07-22 19:33:46+00	78c0bf35-ec22-44d0-a84d-78644404206b
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-22 19:33:46+00	dfe396e2-2846-473e-abf0-51382ec64cb5
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:33:46+00	45fbbb85-4178-4864-8a61-8909e2a81ce7
aws	gpu	A10G	24.00	\N	\N	1.490300	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:33:46+00	8d085fb5-aa04-4267-9e9a-ab7758da4a96
aws	gpu	T4	16.00	\N	\N	0.647000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:33:46+00	b704cccd-a1d8-4225-8748-5792bcfd157a
aws	gpu	INFERENTIA2	32.00	\N	\N	0.909800	available	https://aws.amazon.com/ec2/instance-types/inf2/	32.00	250.00	2026-07-22 19:33:46+00	c0f9a785-ce31-4678-817e-fe9a1ab9be73
aws	gpu	A10G	24.00	\N	\N	1.996900	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:33:46+00	6281da90-d662-44ba-b1ab-21c072fec942
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-22 19:33:46+00	1cf94e71-e0ff-4118-90ae-799892a55ced
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:33:46+00	3565bf6a-7e74-433d-b88b-a818b04931c3
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-22 19:33:46+00	eac41e1c-5cd6-42dc-8b4e-8329da7963b8
aws	gpu	A10G	24.00	\N	\N	5.036500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:33:46+00	465c84d6-6387-4573-a0d3-7fbc64135000
aws	gpu	A10G	24.00	\N	\N	1.237000	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-22 19:33:46+00	fcc0c9a2-0f39-487b-8715-ada2873fd148
aws	gpu	T4	16.00	\N	\N	0.925000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-23 09:23:07+00	782f9a28-508b-47fc-9019-d62f7bedb5f7
aws	gpu	A10G	24.00	\N	\N	1.996900	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-23 09:23:07+00	b5bdc011-279d-431f-92e0-52bbb6b7bcbd
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-23 09:23:07+00	8b44ee7a-dd15-45a1-8bc5-f503aac3c68e
aws	gpu	A10G	24.00	\N	\N	3.010100	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-23 09:23:07+00	575416a2-9c2b-49b1-a5c9-5d7fffc9b746
aws	gpu	1	16.00	\N	\N	1.018500	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-23 09:23:07+00	5b476091-d38b-4f23-a553-4a22c1e93f98
aws	gpu	A10G	24.00	\N	\N	3.010100	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-23 09:23:07+00	7b79258c-01c8-4c9e-b50a-59997f1f80ce
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-23 09:23:07+00	a4472fb8-f3c0-4f3b-9ac6-d14272e7e020
aws	gpu	T4	16.00	\N	\N	1.481000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-23 09:23:07+00	47c3c745-34d9-47e1-96f0-ba25d6c472a4
aws	gpu	1	16.00	\N	\N	0.683900	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-23 09:23:07+00	d06ca94f-6539-45d6-8ae5-c5196b281149
aws	gpu	1	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-23 09:23:07+00	5d637140-454e-4ace-9ad9-5d5d9e013625
aws	gpu	1	16.00	\N	\N	0.683900	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-23 09:23:07+00	9225444b-4b06-4b0d-9b4c-ba19deccc8ec
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-23 09:23:07+00	f3c4459e-2fb8-457a-90f6-1e2eb84099b0
aws	gpu	T4	16.00	\N	\N	0.647000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-23 09:23:07+00	62b61718-2cec-4da0-848f-a752f8285901
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-23 09:23:07+00	2be5978b-beaf-4bac-a97c-cfce8a54c285
aws	gpu	T4	16.00	\N	\N	5.353000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-23 09:23:07+00	b6f24ce9-0ac1-4f48-8801-76ea13e7bd4c
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-23 09:23:07+00	c8afe46a-e769-4c78-96d6-19aec2a5c169
aws	gpu	A10G	24.00	\N	\N	1.743600	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-23 09:23:07+00	5f170484-f8e0-40ce-8cfb-5138ef363cf1
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-23 09:23:07+00	5d42003a-2b72-47b7-be41-c65acf5cf651
aws	gpu	1	16.00	\N	\N	1.018500	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-23 09:23:07+00	c51e16ad-71e0-46a2-86b3-9c9b57f91546
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-23 09:23:07+00	02ddcf5c-d2b9-403a-a623-35081789cb92
aws	gpu	T4	16.00	\N	\N	2.677000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-23 09:23:07+00	98ebb209-7a64-403e-a0dd-9ecc1421687d
aws	gpu	T4	16.00	\N	\N	1.481000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-23 09:23:07+00	78b6a94a-33ff-4977-a2da-4f7e1c52f7c7
aws	gpu	T4	16.00	\N	\N	5.353000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-23 09:23:07+00	5f74a8c8-6e64-4789-b0d5-0d39688fc1c2
aws	gpu	A10G	24.00	\N	\N	5.036500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-23 09:23:07+00	76bf1b6c-628e-4f69-ae97-9a34e94b7137
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-23 09:23:07+00	ccd55a86-0db3-4386-ab75-58736b5bbe8c
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-23 09:23:07+00	fa0512ac-8c76-44b6-bf39-cc0c4b550c12
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-23 09:23:07+00	a7ddeeda-4514-4161-83fa-40bf7dd1ec0c
aws	gpu	T4	16.00	\N	\N	0.925000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-23 09:23:07+00	7f60ee81-4428-4803-9b3f-1fb8267ba8c2
aws	gpu	A100	40.00	\N	\N	3.801300	available	https://aws.amazon.com/ec2/instance-types/p4d/	128.00	400.00	2026-07-23 09:23:07+00	4056ed1b-5040-4cdc-b1bd-a24db499c655
aws	gpu	A10G	24.00	\N	\N	1.743600	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-23 09:23:07+00	ec89f161-6b55-49bc-9b5c-26ae46a07ecc
aws	gpu	1	16.00	\N	\N	0.516600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-23 09:23:07+00	5fa76a85-5f24-479a-bf90-0275b936c5e6
aws	gpu	A10G	24.00	\N	\N	1.490300	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-23 09:23:07+00	dd7a95bf-3cc2-40b7-88a3-326a23be0565
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-23 09:23:07+00	c85e071c-e0dd-4046-8e9c-faa1cba45e9f
aws	gpu	A10G	24.00	\N	\N	1.237000	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-23 09:23:07+00	dab478ad-6af5-4967-86d4-30d843ae7d68
aws	gpu	1	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-23 09:23:07+00	99cb845b-a8f9-44ea-a494-70afc5be9a98
aws	gpu	T4	16.00	\N	\N	2.677000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-23 09:23:07+00	e8ad667c-fef4-4c70-b4ca-91452df22df7
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-23 09:23:07+00	18623191-fe56-4ea4-8c53-b572e8bd35f6
aws	gpu	A100	40.00	\N	\N	3.801300	available	https://aws.amazon.com/ec2/instance-types/p4d/	128.00	400.00	2026-07-23 09:23:07+00	fadc937f-9636-43ad-b681-cc56dd368257
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-23 09:23:07+00	a8dc84fd-9de6-45ee-bb9a-08e14c0ecac4
aws	gpu	1	16.00	\N	\N	0.516600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-23 09:23:07+00	620eface-1765-4db7-9c78-8ce3aa5f9dca
aws	gpu	INFERENTIA2	32.00	\N	\N	0.909800	available	https://aws.amazon.com/ec2/instance-types/inf2/	32.00	250.00	2026-07-23 09:23:07+00	ac8e31be-5622-495a-adec-37af57da6f72
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-23 09:23:07+00	897856a2-490d-46c1-af4b-2e05c3b3d431
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-23 09:23:07+00	fc6f4b43-871c-4d1d-b833-366c5d66ba6d
aws	gpu	A10G	24.00	\N	\N	1.490300	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-23 09:23:07+00	5633c4c8-e677-42d1-b834-71deb44870f0
aws	gpu	T4	16.00	\N	\N	0.647000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-23 09:23:07+00	fd36ff74-5631-4db6-b7c1-26bc0f1b25aa
aws	gpu	INFERENTIA2	32.00	\N	\N	0.909800	available	https://aws.amazon.com/ec2/instance-types/inf2/	32.00	250.00	2026-07-23 09:23:07+00	1662c77a-1e30-41f1-a492-3ab4f0d885b3
aws	gpu	A10G	24.00	\N	\N	1.996900	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-23 09:23:07+00	facdd712-83bd-4c80-a309-8175518feb83
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-23 09:23:07+00	62a68783-6aa6-4d75-902b-699537208fef
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-23 09:23:07+00	01ded9da-6a49-4dab-ba13-e9174f437ddd
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-23 09:23:07+00	a6e83224-da05-46c5-a78f-3a9c07d926a7
aws	gpu	A10G	24.00	\N	\N	5.036500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-23 09:23:07+00	959776e2-94e1-4713-a1f7-591fcef863ec
aws	gpu	A10G	24.00	\N	\N	1.237000	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-23 09:23:07+00	66b24abf-fec7-4bd1-bf0b-f4ca658e0745
aws	gpu	T4	16.00	\N	\N	0.925000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-23 09:31:06+00	2ce5e943-834d-43d0-b7d3-568b39cda784
aws	gpu	A10G	24.00	\N	\N	1.996900	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-23 09:31:06+00	6b0c8e34-e3fa-46b1-ad69-f55c4d3198d3
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-23 09:31:06+00	d382268b-a31e-45c3-bef9-b41fabbe0157
aws	gpu	A10G	24.00	\N	\N	3.010100	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-23 09:31:06+00	69cb4696-b89b-41e7-ada3-39f73a4c8130
aws	gpu	1	16.00	\N	\N	1.018500	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-23 09:31:06+00	8e8cb3c8-d3ab-43aa-ab3c-ac378f0e200a
aws	gpu	A10G	24.00	\N	\N	3.010100	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-23 09:31:06+00	c4b9064e-665c-42ab-89ff-b5a8aaad5222
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-23 09:31:06+00	453062f9-ca36-4281-91d4-caad95bf46bc
aws	gpu	T4	16.00	\N	\N	1.481000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-23 09:31:06+00	5ebc39e9-ff5f-412c-8647-e61761fb8d2a
aws	gpu	1	16.00	\N	\N	0.683900	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-23 09:31:06+00	172416ed-d859-43b2-8534-f7a9dd9ce9fe
aws	gpu	1	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-23 09:31:06+00	bbfada17-91d1-478d-88de-d9597e80515d
aws	gpu	1	16.00	\N	\N	0.683900	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-23 09:31:06+00	50db0e6e-536a-49bb-99c7-d7746ae4d038
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-23 09:31:06+00	871cbcab-2397-4633-aacf-4273ccc4d107
aws	gpu	T4	16.00	\N	\N	0.647000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-23 09:31:06+00	e14a1d79-091a-4c01-b662-936ff11b834f
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-23 09:31:06+00	71328368-f4b0-46c2-b44d-78c8e4661489
aws	gpu	T4	16.00	\N	\N	5.353000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-23 09:31:06+00	a5b6e188-0d72-41c0-9923-b20b098e0b65
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-23 09:31:06+00	9cafdbbe-e134-4de6-99a9-3f31234ebcb7
aws	gpu	A10G	24.00	\N	\N	1.743600	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-23 09:31:06+00	216e41a7-39d6-4b00-89fa-aaeeb06c60e0
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-23 09:31:06+00	d18c3cc8-ab8d-43b1-926a-d96f72dded5e
aws	gpu	1	16.00	\N	\N	1.018500	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-23 09:31:06+00	ade2f351-22c5-42ae-8412-34aeab2bc1cb
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-23 09:31:06+00	6e1b7c22-3724-456c-8309-fef756645681
aws	gpu	T4	16.00	\N	\N	2.677000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-23 09:31:06+00	4be08d7a-8e07-4251-af69-d68e95ae5f7e
aws	gpu	T4	16.00	\N	\N	1.481000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-23 09:31:06+00	1a61506b-f99c-416e-9281-d0c3640dd1ef
aws	gpu	T4	16.00	\N	\N	5.353000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-23 09:31:06+00	2caf456d-3cdc-48d4-b4c6-fa529f14851c
aws	gpu	A10G	24.00	\N	\N	5.036500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-23 09:31:06+00	8bff0f22-cfc0-43cd-8be5-47fbb88604ac
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-23 09:31:06+00	5bb056ec-ec60-4888-a6dc-0680d5930f51
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-23 09:31:06+00	d9f94b10-b4ef-430a-ad97-c75112da074e
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-23 09:31:06+00	a820740a-e2db-47c5-833e-e7e9cdb2c169
aws	gpu	T4	16.00	\N	\N	0.925000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-23 09:31:06+00	373c1603-4340-4dfb-9e8a-7dc0b3e0f9b5
aws	gpu	A100	40.00	\N	\N	3.801300	available	https://aws.amazon.com/ec2/instance-types/p4d/	128.00	400.00	2026-07-23 09:31:06+00	dbe46cdb-7c4f-49bc-91fe-3a39fe3286d1
aws	gpu	A10G	24.00	\N	\N	1.743600	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-23 09:31:06+00	322567e9-931d-40cb-9332-c44ccfdf103e
aws	gpu	1	16.00	\N	\N	0.516600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-23 09:31:06+00	c0a27008-d955-48a5-ab6b-650221355f99
aws	gpu	A10G	24.00	\N	\N	1.490300	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-23 09:31:06+00	c1c2e159-913b-4faf-b1fc-8cd10b2a7fdb
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-23 09:31:06+00	e57cf37d-004f-433a-8e84-c9721fe4b0fe
aws	gpu	A10G	24.00	\N	\N	1.237000	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-23 09:31:06+00	74e2b45b-d9bf-4388-b9a3-0e48e5ac5c91
aws	gpu	1	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-23 09:31:06+00	3e2dc385-df36-496e-97ca-bc7f11ed6352
aws	gpu	T4	16.00	\N	\N	2.677000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-23 09:31:06+00	ee6cd802-10f8-4216-a1ac-7cc78fe2d9cd
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-23 09:31:06+00	f3699952-db02-4989-82eb-7dc0b52fb89e
aws	gpu	A100	40.00	\N	\N	3.801300	available	https://aws.amazon.com/ec2/instance-types/p4d/	128.00	400.00	2026-07-23 09:31:06+00	f10e584c-5341-474a-931b-ae2c5c1fa1cb
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-23 09:31:06+00	ebd6f551-ec4c-437c-a6cf-3f3175547b32
aws	gpu	1	16.00	\N	\N	0.516600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-23 09:31:06+00	4c548661-c9c4-4651-9779-71dc89f20fa7
aws	gpu	INFERENTIA2	32.00	\N	\N	0.909800	available	https://aws.amazon.com/ec2/instance-types/inf2/	32.00	250.00	2026-07-23 09:31:06+00	d2c8f32b-1518-4c40-94c7-0974d09e6c08
aws	gpu	V100	16.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	64.00	300.00	2026-07-23 09:31:06+00	191b9004-f532-4afd-a886-705e984bc9e0
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-23 09:31:06+00	e6342ed9-e68b-46ed-bf20-cd304a5b6d98
aws	gpu	A10G	24.00	\N	\N	1.490300	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-23 09:31:06+00	f8ccb813-8f4d-4cdc-a336-2298f4f56424
aws	gpu	T4	16.00	\N	\N	0.647000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-23 09:31:06+00	b4405028-13f8-4393-b35d-be1f335200d5
aws	gpu	INFERENTIA2	32.00	\N	\N	0.909800	available	https://aws.amazon.com/ec2/instance-types/inf2/	32.00	250.00	2026-07-23 09:31:06+00	b7eeb705-3522-46a6-8246-f09d0c0a06d0
aws	gpu	A10G	24.00	\N	\N	1.996900	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-23 09:31:06+00	c208f265-c0e4-45d3-ae3c-d5a718908191
aws	gpu	2	16.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	32.00	250.00	2026-07-23 09:31:06+00	5fb63f3e-50c4-4330-a2a6-0ab0264ceff5
aws	gpu	A10G	24.00	\N	\N	2.503500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-23 09:31:06+00	711fcf46-5e5f-495a-b8f6-b03bd8519879
aws	gpu	T4	16.00	\N	\N	1.203000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	32.00	250.00	2026-07-23 09:31:06+00	63b27e1c-99cf-4922-9487-88db9a55030c
aws	gpu	A10G	24.00	\N	\N	5.036500	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-23 09:31:06+00	e61ab530-618f-44f9-a874-852592f8869c
aws	gpu	A10G	24.00	\N	\N	1.237000	available	https://aws.amazon.com/ec2/instance-types/g5/	32.00	250.00	2026-07-23 09:31:06+00	122217a8-ef38-46ba-8d4e-add95edee21a
unknown	gpu	A100 40GB	40.00	\N	\N	0.350000	available	https://cloudv.kr/server/gpu.html	128.00	400.00	2026-07-22 18:01:12+00	a521eda7-1fb5-4d05-9b25-43c68fd9a18b
unknown	gpu	A100 80GB	80.00	\N	\N	0.420000	available	https://cloudv.kr/server/gpu.html	128.00	400.00	2026-07-22 18:01:12+00	5427bf55-1ba4-4807-afb3-170b122d5a4a
unknown	gpu	RTX 4090	24.00	\N	\N	0.150000	available	https://cloudv.kr/server/gpu.html	64.00	450.00	2026-07-22 18:01:12+00	3ce8beca-18d1-4dcf-b2fd-065f3498554a
unknown	gpu	RTX 3090	24.00	\N	\N	0.100000	available	https://cloudv.kr/server/gpu.html	48.00	350.00	2026-07-22 18:01:12+00	120f92dd-98e2-4e22-ba1e-1b8cf4f6ab1a
unknown	gpu	A100 40GB	40.00	\N	\N	0.350000	available	https://cloudv.kr/server/gpu.html	128.00	400.00	2026-07-22 19:09:23+00	4d506451-3db3-4759-92de-e94b28afbc18
unknown	gpu	A100 80GB	80.00	\N	\N	0.420000	available	https://cloudv.kr/server/gpu.html	128.00	400.00	2026-07-22 19:09:23+00	127844fa-3b21-47b6-a41f-c04e3328989b
unknown	gpu	RTX 4090	24.00	\N	\N	0.150000	available	https://cloudv.kr/server/gpu.html	64.00	450.00	2026-07-22 19:09:23+00	2544f082-e202-4e67-9b28-e9b84d30ac7f
unknown	gpu	RTX 3090	24.00	\N	\N	0.100000	available	https://cloudv.kr/server/gpu.html	48.00	350.00	2026-07-22 19:09:23+00	3db27106-5a95-40e5-a293-6d9fc7da90b4
cloudv	gpu	A100 40GB	40.00	\N	\N	0.350000	available	https://cloudv.kr/server/gpu.html	128.00	400.00	2026-07-22 19:19:17+00	bad5f3ee-4702-468b-96ce-5e8e7c2b13cc
cloudv	gpu	A100 80GB	80.00	\N	\N	0.420000	available	https://cloudv.kr/server/gpu.html	128.00	400.00	2026-07-22 19:19:17+00	1e249af0-f891-45f5-be64-60846e9a408c
cloudv	gpu	RTX 4090	24.00	\N	\N	0.150000	available	https://cloudv.kr/server/gpu.html	64.00	450.00	2026-07-22 19:19:17+00	47fb4222-16b9-4b80-a20a-39f84803506b
cloudv	gpu	RTX 3090	24.00	\N	\N	0.100000	available	https://cloudv.kr/server/gpu.html	48.00	350.00	2026-07-22 19:19:17+00	57758500-83a7-471f-82ac-db7679395fc0
cloudv	gpu	A100 40GB	40.00	\N	\N	0.350000	available	https://cloudv.kr/server/gpu.html	128.00	400.00	2026-07-22 19:33:47+00	39f65b00-c455-447c-9fbc-7fb1861da86a
cloudv	gpu	A100 80GB	80.00	\N	\N	0.420000	available	https://cloudv.kr/server/gpu.html	128.00	400.00	2026-07-22 19:33:47+00	fb73b021-fa1d-4150-ab5c-c92a646b0a1d
cloudv	gpu	RTX 4090	24.00	\N	\N	0.150000	available	https://cloudv.kr/server/gpu.html	64.00	450.00	2026-07-22 19:33:47+00	613167f4-3ebf-49b0-889a-1fa3bb8ddddd
cloudv	gpu	RTX 3090	24.00	\N	\N	0.100000	available	https://cloudv.kr/server/gpu.html	48.00	350.00	2026-07-22 19:33:47+00	99e47d42-8472-452b-8414-5efd4c9907fb
cloudv	gpu	A100 40GB	40.00	\N	\N	0.350000	available	https://cloudv.kr/server/gpu.html	128.00	400.00	2026-07-23 09:23:30+00	993524fd-a5a7-465c-b87b-919ecabd11bb
cloudv	gpu	A100 80GB	80.00	\N	\N	0.420000	available	https://cloudv.kr/server/gpu.html	128.00	400.00	2026-07-23 09:23:30+00	b5ee5fb3-023b-482b-aa7c-6c907e326773
cloudv	gpu	RTX 4090	24.00	\N	\N	0.150000	available	https://cloudv.kr/server/gpu.html	64.00	450.00	2026-07-23 09:23:30+00	41e36a96-e1e5-4827-921e-6c482039c248
cloudv	gpu	RTX 3090	24.00	\N	\N	0.100000	available	https://cloudv.kr/server/gpu.html	48.00	350.00	2026-07-23 09:23:30+00	cc75f582-cca5-4da2-a70e-cd854e744459
cloudv	gpu	A100 40GB	40.00	\N	\N	0.350000	available	https://cloudv.kr/server/gpu.html	128.00	400.00	2026-07-23 09:31:27+00	86d64a48-0686-4953-b659-49e7f88fadca
cloudv	gpu	A100 80GB	80.00	\N	\N	0.420000	available	https://cloudv.kr/server/gpu.html	128.00	400.00	2026-07-23 09:31:27+00	174745e4-8bcd-4da8-8f2b-c6946ec3ef6a
cloudv	gpu	RTX 4090	24.00	\N	\N	0.150000	available	https://cloudv.kr/server/gpu.html	64.00	450.00	2026-07-23 09:31:27+00	9c686463-61b8-4d86-bd59-1185bf408719
cloudv	gpu	RTX 3090	24.00	\N	\N	0.100000	available	https://cloudv.kr/server/gpu.html	48.00	350.00	2026-07-23 09:31:27+00	efc01daa-8b29-4198-a78b-d655d3778e56
unknown	gpu	A100 80GB	80.00	\N	\N	0.850000	available	https://www.gabia.com/	128.00	400.00	2026-07-22 18:01:13+00	1ee40636-2b16-4fbb-b11e-62f8fa15fb08
unknown	gpu	V100	32.00	\N	\N	0.400000	available	https://www.gabia.com/	64.00	300.00	2026-07-22 18:01:13+00	3e8a7f36-0cf1-4e30-8d1d-2827c9a9c89e
unknown	gpu	A100 80GB	80.00	\N	\N	0.850000	available	https://www.gabia.com/	128.00	400.00	2026-07-22 19:09:24+00	55885032-409e-4138-8479-e0aa87317b48
unknown	gpu	V100	32.00	\N	\N	0.400000	available	https://www.gabia.com/	64.00	300.00	2026-07-22 19:09:24+00	d1366a92-abcf-4058-99c4-79a71caa498b
gabia	gpu	A100 80GB	80.00	\N	\N	0.850000	available	https://www.gabia.com/	128.00	400.00	2026-07-22 19:19:18+00	d8521db6-9bbf-43a3-9e70-42be2897cf95
gabia	gpu	V100	32.00	\N	\N	0.400000	available	https://www.gabia.com/	64.00	300.00	2026-07-22 19:19:18+00	5b083e43-c879-4a2a-b3e5-ec2b9e755614
gabia	gpu	A100 80GB	80.00	\N	\N	0.850000	available	https://www.gabia.com/	128.00	400.00	2026-07-22 19:33:48+00	94b96eb5-1976-4317-a8e1-8fc877807dc5
gabia	gpu	V100	32.00	\N	\N	0.400000	available	https://www.gabia.com/	64.00	300.00	2026-07-22 19:33:48+00	8e1c0d89-7274-4cbd-b351-579eb8fae4b7
gabia	gpu	A100 80GB	80.00	\N	\N	0.850000	available	https://www.gabia.com/	128.00	400.00	2026-07-23 09:23:42+00	1cc379cf-cc49-4410-8c77-51fa6d093479
gabia	gpu	V100	32.00	\N	\N	0.400000	available	https://www.gabia.com/	64.00	300.00	2026-07-23 09:23:42+00	84c7cc43-1246-43da-91dc-3bfa31da605c
gabia	gpu	A100 80GB	80.00	\N	\N	0.850000	available	https://www.gabia.com/	128.00	400.00	2026-07-23 09:32:32+00	05992f7e-2daa-461a-9c98-29c745aba059
gabia	gpu	V100	32.00	\N	\N	0.400000	available	https://www.gabia.com/	64.00	300.00	2026-07-23 09:32:32+00	569a2dff-1019-4f81-b3b5-288c0fb9e175
unknown	gpu	H100 SXM	80.00	\N	\N	2.390000	available	https://gpuaas.kr/	256.00	700.00	2026-07-22 18:01:11+00	c463c9de-f90f-41ae-906b-cea88c49ccfb
unknown	gpu	A100 SXM	80.00	\N	\N	1.550000	available	https://gpuaas.kr/	128.00	400.00	2026-07-22 18:01:11+00	209748b1-14bb-468c-a5ca-ab29c4211f0a
unknown	gpu	L40S	48.00	\N	\N	1.800000	available	https://gpuaas.kr/	128.00	350.00	2026-07-22 18:01:11+00	d5ccf011-78c6-416a-a6be-db1588d37916
unknown	gpu	H100 SXM	80.00	\N	\N	2.390000	available	https://gpuaas.kr/	256.00	700.00	2026-07-22 19:09:23+00	3e9a97be-2b5c-4cce-818d-39baf5359ab7
unknown	gpu	A100 SXM	80.00	\N	\N	1.550000	available	https://gpuaas.kr/	128.00	400.00	2026-07-22 19:09:23+00	b0d3f3f4-e774-4728-956f-ebb14b733254
unknown	gpu	L40S	48.00	\N	\N	1.800000	available	https://gpuaas.kr/	128.00	350.00	2026-07-22 19:09:23+00	5ddbe7a5-3983-4771-9492-dcdda30f7657
gpuaas	gpu	H100 SXM	80.00	\N	\N	2.390000	available	https://gpuaas.kr/	256.00	700.00	2026-07-22 19:19:16+00	5a18a937-45b4-43a6-9561-1346d031b6e3
gpuaas	gpu	A100 SXM	80.00	\N	\N	1.550000	available	https://gpuaas.kr/	128.00	400.00	2026-07-22 19:19:16+00	9fff657f-3a17-4399-b68c-cc85c61a9d02
gpuaas	gpu	L40S	48.00	\N	\N	1.800000	available	https://gpuaas.kr/	128.00	350.00	2026-07-22 19:19:16+00	91ded474-4195-42d1-a40f-c0448b90f15f
gpuaas	gpu	H100 SXM	80.00	\N	\N	2.390000	available	https://gpuaas.kr/	256.00	700.00	2026-07-22 19:33:46+00	5d3048ac-2dd3-4444-90e8-1edee6441b8b
gpuaas	gpu	A100 SXM	80.00	\N	\N	1.550000	available	https://gpuaas.kr/	128.00	400.00	2026-07-22 19:33:46+00	cecb524f-0417-4b8a-a4a3-8c9e22db492e
gpuaas	gpu	L40S	48.00	\N	\N	1.800000	available	https://gpuaas.kr/	128.00	350.00	2026-07-22 19:33:46+00	d6dfb4ee-ffd3-431d-9eff-82bbb53d1722
gpuaas	gpu	H100 SXM	80.00	\N	\N	2.390000	available	https://gpuaas.kr/	256.00	700.00	2026-07-23 09:23:21+00	2214efb6-06ce-49a3-9932-e2671ec7375b
gpuaas	gpu	A100 SXM	80.00	\N	\N	1.550000	available	https://gpuaas.kr/	128.00	400.00	2026-07-23 09:23:21+00	a361051c-e9d0-46fe-bda1-0c3c86840028
gpuaas	gpu	L40S	48.00	\N	\N	1.800000	available	https://gpuaas.kr/	128.00	350.00	2026-07-23 09:23:21+00	098854f9-3c43-499f-bf1a-c99ae13ff6b4
gpuaas	gpu	H100 SXM	80.00	\N	\N	2.390000	available	https://gpuaas.kr/	256.00	700.00	2026-07-23 09:31:20+00	d4f73e6c-57aa-4daa-936b-eb0eaaf560b7
gpuaas	gpu	A100 SXM	80.00	\N	\N	1.550000	available	https://gpuaas.kr/	128.00	400.00	2026-07-23 09:31:20+00	28bc4097-dc40-40e1-84d0-7be1fd357271
gpuaas	gpu	L40S	48.00	\N	\N	1.800000	available	https://gpuaas.kr/	128.00	350.00	2026-07-23 09:31:20+00	0e1aedb4-716e-4176-8626-731f7c6f94dc
unknown	gpu	H100	80.00	\N	\N	3.000000	available	https://cloud.kt.com/	256.00	700.00	2026-07-22 18:01:14+00	065f35bc-3b98-4d97-827d-bde25804abd8
unknown	gpu	A100	40.00	\N	\N	1.900000	available	https://cloud.kt.com/	128.00	400.00	2026-07-22 18:01:14+00	177feea7-aa02-49b6-baa7-b21f7adea064
unknown	gpu	V100	16.00	\N	\N	0.600000	available	https://cloud.kt.com/	64.00	300.00	2026-07-22 18:01:14+00	46b2b6f1-0eb5-4145-8f0e-2ab9e8191cad
unknown	gpu	H100	80.00	\N	\N	3.000000	available	https://cloud.kt.com/	256.00	700.00	2026-07-22 19:09:25+00	6b00306b-5198-433e-a840-0977d5c654c8
unknown	gpu	A100	40.00	\N	\N	1.900000	available	https://cloud.kt.com/	128.00	400.00	2026-07-22 19:09:25+00	7128853d-d1bc-4597-93c8-53315807ce1d
unknown	gpu	V100	16.00	\N	\N	0.600000	available	https://cloud.kt.com/	64.00	300.00	2026-07-22 19:09:25+00	d704790b-658b-4165-a0ff-5f5fb82bedb2
ktcloud	gpu	H100	80.00	\N	\N	3.000000	available	https://cloud.kt.com/	256.00	700.00	2026-07-22 19:19:18+00	f823be8c-2959-4893-b84f-a48a7f42c1ce
ktcloud	gpu	A100	40.00	\N	\N	1.900000	available	https://cloud.kt.com/	128.00	400.00	2026-07-22 19:19:18+00	eea06c14-5ea1-437b-8088-327967549ab6
ktcloud	gpu	V100	16.00	\N	\N	0.600000	available	https://cloud.kt.com/	64.00	300.00	2026-07-22 19:19:18+00	1a7cc7ad-a3b8-4de5-9936-1cc513ab492d
ktcloud	gpu	H100	80.00	\N	\N	3.000000	available	https://cloud.kt.com/	256.00	700.00	2026-07-22 19:33:48+00	29fee818-9cf1-498d-b015-82c4f353a2d5
ktcloud	gpu	A100	40.00	\N	\N	1.900000	available	https://cloud.kt.com/	128.00	400.00	2026-07-22 19:33:48+00	721a1a7b-b334-4245-bc22-7d29aa4ed64c
ktcloud	gpu	V100	16.00	\N	\N	0.600000	available	https://cloud.kt.com/	64.00	300.00	2026-07-22 19:33:48+00	1450ba9d-01ca-4e83-9cbb-bb63c3558dbd
ktcloud	gpu	H100	80.00	\N	\N	3.000000	available	https://cloud.kt.com/	256.00	700.00	2026-07-23 09:23:47+00	30f32fdd-f41a-4ed3-aa9e-e5b801b2cec6
ktcloud	gpu	A100	40.00	\N	\N	1.900000	available	https://cloud.kt.com/	128.00	400.00	2026-07-23 09:23:47+00	00638d87-5d26-4f9d-821a-26f4ee6beb94
ktcloud	gpu	V100	16.00	\N	\N	0.600000	available	https://cloud.kt.com/	64.00	300.00	2026-07-23 09:23:47+00	5966311c-0c94-4187-a961-9b22eb0648df
ktcloud	gpu	H100	80.00	\N	\N	3.000000	available	https://cloud.kt.com/	256.00	700.00	2026-07-23 09:32:38+00	7ef4ef6a-ae85-49e4-b443-cd8d3a26ce68
ktcloud	gpu	A100	40.00	\N	\N	1.900000	available	https://cloud.kt.com/	128.00	400.00	2026-07-23 09:32:38+00	22cfc702-101b-4c5d-a36b-8466bd5666c1
ktcloud	gpu	V100	16.00	\N	\N	0.600000	available	https://cloud.kt.com/	64.00	300.00	2026-07-23 09:32:38+00	ab4d9db1-55df-4410-b959-48272a6cc7f3
ncloud	gpu	V100	32.00	\N	\N	2.100000	available	https://www.ncloud.com/product/compute/gpuServer	64.00	300.00	2026-07-22 20:22:58+00	73e42b3b-c3ee-4694-bb37-313e786c3051
ncloud	gpu	T4	16.00	\N	\N	0.800000	available	https://www.ncloud.com/product/compute/gpuServer	32.00	250.00	2026-07-22 20:22:58+00	ff6b87ba-3fd9-499c-a75f-dfc1f4a8cfa3
ncloud	gpu	TESLA V100 (1X)	32.00	\N	\N	1.850000	available	https://www.ncloud.com/product/compute/gpuServer	64.00	300.00	2026-07-22 20:25:18+00	378b3acb-6d31-49a5-8812-d6d5fd299846
ncloud	gpu	TESLA T4 (1X)	16.00	\N	\N	0.600000	available	https://www.ncloud.com/product/compute/gpuServer	32.00	250.00	2026-07-22 20:25:18+00	991dfa15-d70f-48db-ac91-8a60d2150459
ncloud	gpu	A100 (베어메탈)	40.00	\N	\N	2.200000	available	https://www.ncloud.com/product/compute/gpuServer	128.00	400.00	2026-07-22 20:25:18+00	2c7cacb0-405a-42bb-bf5d-c60fbf4f83af
unknown	gpu	AMD INSTINCT MI300X OAM	192.00	\N	\N	2.390000	available	\N	\N	\N	2026-07-22 16:50:59+00	8c436089-6e1f-4b2e-a2bb-f9c81252bf4a
unknown	gpu	NVIDIA A100 80GB PCIE	80.00	\N	\N	1.390000	available	\N	\N	\N	2026-07-22 16:50:59+00	dda24270-428b-4f17-87b6-a6084656aee2
unknown	gpu	NVIDIA A100-SXM4-80GB	80.00	\N	\N	1.490000	available	\N	\N	\N	2026-07-22 16:50:59+00	973bbd6d-c9d6-4a72-a1bb-4dcb0fe45704
unknown	gpu	NVIDIA A40	48.00	\N	\N	0.440000	available	\N	\N	\N	2026-07-22 16:50:59+00	0d1e4f51-de64-491b-8bcb-0594114ff409
unknown	gpu	NVIDIA B200	180.00	\N	\N	5.890000	available	\N	\N	\N	2026-07-22 16:50:59+00	bf0ba219-32a3-47b8-9908-e23885e40f66
unknown	gpu	NVIDIA B300 SXM6 AC	288.00	\N	\N	7.390000	available	\N	\N	\N	2026-07-22 16:50:59+00	95e12fb2-bdb5-424b-9681-9b38f3104a9f
unknown	gpu	NVIDIA GEFORCE GTX 1050 TI	4.00	\N	\N	0.500000	available	\N	\N	\N	2026-07-22 16:50:59+00	0605c566-e363-4558-b9dd-2056be05c761
unknown	gpu	NVIDIA GEFORCE RTX 3090	24.00	\N	\N	0.500000	available	\N	\N	\N	2026-07-22 16:50:59+00	42c5a9d5-04d5-4205-b629-af6a93fde169
unknown	gpu	NVIDIA GEFORCE RTX 3090 TI	24.00	\N	\N	0.460000	available	\N	\N	\N	2026-07-22 16:50:59+00	93487d5f-7073-46a6-8227-16f1b412510f
unknown	gpu	NVIDIA GEFORCE RTX 4070 TI	12.00	\N	\N	0.500000	available	\N	\N	\N	2026-07-22 16:50:59+00	fe35c106-4b09-4307-9a1e-63b2b3d643ff
unknown	gpu	NVIDIA GEFORCE RTX 4080	16.00	\N	\N	0.500000	available	\N	\N	\N	2026-07-22 16:50:59+00	619a1a5d-e5f9-4d17-a6fc-3db8ccbc2c86
unknown	gpu	NVIDIA GEFORCE RTX 4080 SUPER	16.00	\N	\N	0.500000	available	\N	\N	\N	2026-07-22 16:50:59+00	3961f5d1-f544-4239-a35e-b54ce1eba3b8
unknown	gpu	NVIDIA GEFORCE RTX 4090	24.00	\N	\N	0.690000	available	\N	\N	\N	2026-07-22 16:50:59+00	3361db97-7288-4e95-9137-c6186dea17b5
unknown	gpu	NVIDIA GEFORCE RTX 5080	16.00	\N	\N	0.590000	available	\N	\N	\N	2026-07-22 16:50:59+00	d4f9e692-c902-49b3-b1bc-e2628fc5140f
unknown	gpu	NVIDIA GEFORCE RTX 5090	32.00	\N	\N	0.990000	available	\N	\N	\N	2026-07-22 16:50:59+00	79c70592-3512-4a50-a8c6-a92f72e5e209
unknown	gpu	NVIDIA H100 80GB HBM3	80.00	\N	\N	2.990000	available	\N	\N	\N	2026-07-22 16:50:59+00	804d0295-1e2b-4e29-ac9b-dec8f207844c
unknown	gpu	NVIDIA H100 NVL	94.00	\N	\N	3.190000	available	\N	\N	\N	2026-07-22 16:50:59+00	0123ec8c-5e7b-4c58-af0c-31563757dace
unknown	gpu	NVIDIA H100 PCIE	80.00	\N	\N	2.890000	available	\N	\N	\N	2026-07-22 16:50:59+00	fc570d86-c83d-4715-94fd-569b3a5e7866
unknown	gpu	NVIDIA H200	141.00	\N	\N	4.390000	available	\N	\N	\N	2026-07-22 16:50:59+00	17585946-f71d-4aef-aad5-b92bc5a0d279
unknown	gpu	NVIDIA H200 NVL	143.00	\N	\N	3.790000	available	\N	\N	\N	2026-07-22 16:50:59+00	eb7e1d8c-1dec-47dc-9fb0-2ef5c98ded81
unknown	gpu	NVIDIA L4	24.00	\N	\N	0.390000	available	\N	\N	\N	2026-07-22 16:50:59+00	83910fa1-a8dc-481f-ba66-42c2892a4577
unknown	gpu	NVIDIA L40	48.00	\N	\N	0.820000	available	\N	\N	\N	2026-07-22 16:50:59+00	ed74e79f-c2f9-4165-9157-b9bf35cde6f3
unknown	gpu	NVIDIA L40S	48.00	\N	\N	0.990000	available	\N	\N	\N	2026-07-22 16:50:59+00	22f15c0f-aa90-4591-9fdc-f49b347184a7
unknown	gpu	NVIDIA RTX 2000 ADA GENERATION	16.00	\N	\N	0.240000	available	\N	\N	\N	2026-07-22 16:50:59+00	9ee174f9-7a76-4dde-b7b8-9c3a8a2cdc7e
unknown	gpu	NVIDIA RTX 4000 ADA GENERATION	20.00	\N	\N	0.280000	available	\N	\N	\N	2026-07-22 16:50:59+00	7b78b31a-e503-4f3a-add3-44656798fec9
unknown	gpu	NVIDIA RTX 4000 SFF ADA GENERATION	20.00	\N	\N	0.440000	available	\N	\N	\N	2026-07-22 16:50:59+00	aaf2cef5-ee22-44c0-b72f-54b7e3ebe641
unknown	gpu	NVIDIA RTX 5000 ADA GENERATION	32.00	\N	\N	0.830000	available	\N	\N	\N	2026-07-22 16:50:59+00	a0bc7aae-4841-4dba-9b7a-3031188766d1
unknown	gpu	NVIDIA RTX 6000 ADA GENERATION	48.00	\N	\N	0.840000	available	\N	\N	\N	2026-07-22 16:50:59+00	92907869-0857-4f06-ac01-1f7e8bd519dd
unknown	gpu	NVIDIA RTX A2000	6.00	\N	\N	0.500000	available	\N	\N	\N	2026-07-22 16:50:59+00	83a65572-6896-4bda-9947-a8cccd7cb3ea
unknown	gpu	NVIDIA RTX A4000	16.00	\N	\N	0.250000	available	\N	\N	\N	2026-07-22 16:50:59+00	ef5a3218-1ae8-4815-968f-0dd88a912160
unknown	gpu	NVIDIA RTX A4500	20.00	\N	\N	0.250000	available	\N	\N	\N	2026-07-22 16:50:59+00	ce93cbb0-8b48-484c-95ca-28bec3fc8120
unknown	gpu	NVIDIA RTX A5000	24.00	\N	\N	0.270000	available	\N	\N	\N	2026-07-22 16:50:59+00	cf5988fc-a621-428a-94c8-8b585f806f25
unknown	gpu	NVIDIA RTX A6000	48.00	\N	\N	0.530000	available	\N	\N	\N	2026-07-22 16:50:59+00	b76a67a0-dcde-445b-812e-c52cb225ec91
unknown	gpu	NVIDIA RTX PRO 4000 BLACKWELL	24.00	\N	\N	0.570000	available	\N	\N	\N	2026-07-22 16:50:59+00	4f420de1-9002-4de7-90c4-ac50d25aea81
unknown	gpu	NVIDIA RTX PRO 4500 BLACKWELL	32.00	\N	\N	0.740000	available	\N	\N	\N	2026-07-22 16:50:59+00	002b53fe-f7ee-412e-b182-286aaa1c01a4
unknown	gpu	NVIDIA RTX PRO 5000 BLACKWELL	48.00	\N	\N	0.960000	available	\N	\N	\N	2026-07-22 16:50:59+00	17197884-ac19-4023-9723-b0652483352b
unknown	gpu	NVIDIA RTX PRO 6000 BLACKWELL MAX-Q WORKSTATION EDITION	96.00	\N	\N	0.500000	available	\N	\N	\N	2026-07-22 16:50:59+00	cbc4644d-8db2-48b7-a754-b0114ea0227b
unknown	gpu	NVIDIA RTX PRO 6000 BLACKWELL SERVER EDITION	96.00	\N	\N	1.990000	available	\N	\N	\N	2026-07-22 16:50:59+00	c893718b-48eb-426a-988e-eac0b416889e
unknown	gpu	NVIDIA RTX PRO 6000 BLACKWELL SERVER EDITION MIG 1G.24GB	24.00	\N	\N	0.490000	available	\N	\N	\N	2026-07-22 16:50:59+00	0af206a0-5150-420f-aa69-1c287193ece2
unknown	gpu	NVIDIA RTX PRO 6000 BLACKWELL SERVER EDITION MIG 2G.48GB	48.00	\N	\N	1.000000	available	\N	\N	\N	2026-07-22 16:50:59+00	c9d2b2c8-c059-4fed-a5a4-fd65d7f93856
unknown	gpu	NVIDIA RTX PRO 6000 BLACKWELL WORKSTATION EDITION	96.00	\N	\N	1.890000	available	\N	\N	\N	2026-07-22 16:50:59+00	b9576b62-dd3a-4c3a-a60e-fc8d9d82d927
unknown	gpu	AMD INSTINCT MI300X OAM	192.00	\N	\N	2.390000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 17:52:57+00	95770c48-aa8b-4d1a-adc2-f193b939362a
unknown	gpu	NVIDIA A100 80GB PCIE	80.00	\N	\N	1.390000	available	https://www.runpod.io/console/gpu-cloud	128.00	400.00	2026-07-22 17:52:57+00	4349baf7-d7e0-4ec3-9d5a-9d8ef1672fe6
unknown	gpu	RTX 3090	24.00	\N	\N	0.121185	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	1191fe59-f839-4c89-b3a7-adf03c821c6b
unknown	gpu	NVIDIA A100-SXM4-80GB	80.00	\N	\N	1.490000	available	https://www.runpod.io/console/gpu-cloud	128.00	400.00	2026-07-22 17:52:57+00	f2955d09-5931-49c9-83b9-b040d93dac78
unknown	gpu	NVIDIA A40	48.00	\N	\N	0.440000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 17:52:57+00	bbecfdfe-40b9-4b98-a4e8-71f4a9997597
unknown	gpu	NVIDIA B200	180.00	\N	\N	5.890000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 17:52:57+00	292aa6ab-7e7b-480b-9b15-169fed144baf
unknown	gpu	NVIDIA B300 SXM6 AC	288.00	\N	\N	7.390000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 17:52:57+00	c3f5717e-972d-4e41-ada1-bd7d07669b7a
unknown	gpu	NVIDIA GEFORCE GTX 1050 TI	4.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 17:52:57+00	47d9dab9-8ad1-441d-a5ba-10453072fcbc
unknown	gpu	NVIDIA GEFORCE RTX 3090	24.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	48.00	350.00	2026-07-22 17:52:57+00	6b57717e-14c7-4016-9e47-64b0fe5ae450
unknown	gpu	NVIDIA GEFORCE RTX 3090 TI	24.00	\N	\N	0.460000	available	https://www.runpod.io/console/gpu-cloud	48.00	350.00	2026-07-22 17:52:57+00	4b690339-d173-4fb1-91f9-2a53f991864c
unknown	gpu	NVIDIA GEFORCE RTX 4070 TI	12.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 17:52:57+00	571d3b75-b960-4762-9c35-47dc21104439
unknown	gpu	NVIDIA GEFORCE RTX 4080	16.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	320.00	2026-07-22 17:52:57+00	3490aa5c-87a9-4052-afe8-3e20fd98e6be
unknown	gpu	NVIDIA GEFORCE RTX 4080 SUPER	16.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	320.00	2026-07-22 17:52:57+00	40f4db9a-424d-44a9-8015-5de0f21fbe23
unknown	gpu	NVIDIA GEFORCE RTX 4090	24.00	\N	\N	0.690000	available	https://www.runpod.io/console/gpu-cloud	64.00	450.00	2026-07-22 17:52:57+00	337f0e14-9cad-4e07-a002-51a22d2b8b5f
unknown	gpu	NVIDIA GEFORCE RTX 5080	16.00	\N	\N	0.590000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 17:52:57+00	7a2860d5-e72f-4ecc-ad86-d0caeb2d1851
unknown	gpu	NVIDIA GEFORCE RTX 5090	32.00	\N	\N	0.990000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 17:52:57+00	ed62e148-1d92-4033-8d8a-c7c5a593c048
unknown	gpu	NVIDIA H100 80GB HBM3	80.00	\N	\N	2.990000	available	https://www.runpod.io/console/gpu-cloud	256.00	700.00	2026-07-22 17:52:57+00	7730553f-804a-4d11-b918-072658726aee
unknown	gpu	NVIDIA H100 NVL	94.00	\N	\N	3.190000	available	https://www.runpod.io/console/gpu-cloud	256.00	700.00	2026-07-22 17:52:57+00	368c10d1-d0c0-49a0-b656-c40d64c4acdc
unknown	gpu	NVIDIA H100 PCIE	80.00	\N	\N	2.890000	available	https://www.runpod.io/console/gpu-cloud	256.00	700.00	2026-07-22 17:52:57+00	be268b62-4f6d-41fe-b24b-aa20e64025ac
unknown	gpu	NVIDIA H200	141.00	\N	\N	4.390000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 17:52:57+00	8dcf5459-f2c8-4f42-ac82-3ca142249244
unknown	gpu	NVIDIA H200 NVL	143.00	\N	\N	3.790000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 17:52:57+00	b88ce7ff-17ed-4179-8198-bf35b14c8228
unknown	gpu	NVIDIA L4	24.00	\N	\N	0.390000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 17:52:57+00	7cc8a8f5-52d8-4b92-a2f7-259475c09f2d
unknown	gpu	NVIDIA L40	48.00	\N	\N	0.820000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 17:52:57+00	f0314513-23e1-407e-ac68-6e085f7a4404
unknown	gpu	NVIDIA L40S	48.00	\N	\N	0.990000	available	https://www.runpod.io/console/gpu-cloud	128.00	350.00	2026-07-22 17:52:57+00	ca5da014-eb9d-43e6-9f30-c4869aef970b
unknown	gpu	NVIDIA RTX 2000 ADA GENERATION	16.00	\N	\N	0.240000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 17:52:57+00	fb69ac22-9bfa-4c96-9280-c4bab2f83f91
unknown	gpu	NVIDIA RTX 4000 ADA GENERATION	20.00	\N	\N	0.280000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 17:52:57+00	1e5381ed-cb40-4639-b395-0b9d33d848b4
unknown	gpu	NVIDIA RTX 4000 SFF ADA GENERATION	20.00	\N	\N	0.440000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 17:52:57+00	3c808f7c-2147-4713-bbc2-e5ad1d67504b
unknown	gpu	NVIDIA RTX 5000 ADA GENERATION	32.00	\N	\N	0.830000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 17:52:57+00	74a9f891-9bc0-42c7-9049-e931e5ca0bbe
unknown	gpu	NVIDIA RTX 6000 ADA GENERATION	48.00	\N	\N	0.840000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 17:52:57+00	64e3dac3-66a4-46d0-9528-62ed75b87834
unknown	gpu	NVIDIA RTX A2000	6.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 17:52:57+00	e692477c-69b2-44ff-925e-8a46e4291843
unknown	gpu	NVIDIA RTX A4000	16.00	\N	\N	0.250000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 17:52:57+00	d7aa69b4-3dff-4add-a0bd-b0771bd07cd0
unknown	gpu	NVIDIA RTX A4500	20.00	\N	\N	0.250000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 17:52:57+00	7945fde0-8e09-4846-8d55-583babb1bf0e
unknown	gpu	NVIDIA RTX A5000	24.00	\N	\N	0.270000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 17:52:57+00	19a9534d-5757-4fba-8284-24be7aef9724
unknown	gpu	NVIDIA RTX A6000	48.00	\N	\N	0.530000	available	https://www.runpod.io/console/gpu-cloud	128.00	300.00	2026-07-22 17:52:57+00	670966db-159b-4733-bd6a-419828dd10a6
unknown	gpu	NVIDIA RTX PRO 4000 BLACKWELL	24.00	\N	\N	0.570000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 17:52:57+00	ff768aa1-990f-4bff-ad87-89059802d2e6
unknown	gpu	NVIDIA RTX PRO 4500 BLACKWELL	32.00	\N	\N	0.740000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 17:52:57+00	6e222464-3e1f-41dd-8a40-416f89317584
unknown	gpu	NVIDIA RTX PRO 5000 BLACKWELL	48.00	\N	\N	0.960000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 17:52:57+00	7cc8e5d5-2905-4110-a704-6895ddf3c144
unknown	gpu	NVIDIA RTX PRO 6000 BLACKWELL MAX-Q WORKSTATION EDITION	96.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 17:52:57+00	a7473cd0-1af3-4786-af9f-243da1fcff24
unknown	gpu	NVIDIA RTX PRO 6000 BLACKWELL SERVER EDITION	96.00	\N	\N	1.990000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 17:52:57+00	0827b70a-fbad-4901-8caa-c4fa3c6c90dd
unknown	gpu	NVIDIA RTX PRO 6000 BLACKWELL SERVER EDITION MIG 1G.24GB	24.00	\N	\N	0.490000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 17:52:57+00	a3f29e9f-0823-4eff-b58a-4b0ac2fb09a8
unknown	gpu	NVIDIA RTX PRO 6000 BLACKWELL SERVER EDITION MIG 2G.48GB	48.00	\N	\N	1.000000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 17:52:57+00	302f407f-5465-4b47-a060-63fb143a8fbe
unknown	gpu	NVIDIA RTX PRO 6000 BLACKWELL WORKSTATION EDITION	96.00	\N	\N	1.890000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 17:52:57+00	9943eff5-4553-471f-b8b7-f3edd9ba0d4e
unknown	gpu	AMD INSTINCT MI300X OAM	192.00	\N	\N	2.390000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:00:46+00	199c6968-801f-40e2-90b5-18dfe6225557
unknown	gpu	NVIDIA A100 80GB PCIE	80.00	\N	\N	1.390000	available	https://www.runpod.io/console/gpu-cloud	128.00	400.00	2026-07-22 18:00:46+00	e87bc77d-c2b7-4967-8036-6357c7dffccd
unknown	gpu	NVIDIA A100-SXM4-80GB	80.00	\N	\N	1.490000	available	https://www.runpod.io/console/gpu-cloud	128.00	400.00	2026-07-22 18:00:46+00	b49fa80e-f4ef-4a2d-94ce-5866d6fec7d2
unknown	gpu	NVIDIA A40	48.00	\N	\N	0.440000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:00:46+00	493feabc-77e4-4088-9c69-24b6e7934d75
unknown	gpu	NVIDIA B200	180.00	\N	\N	5.890000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:00:46+00	fd76c62d-340e-4a50-a1a9-ee16d785bc51
unknown	gpu	NVIDIA B300 SXM6 AC	288.00	\N	\N	7.390000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:00:46+00	f6459821-c3aa-48bb-bee2-aa425da70cf8
unknown	gpu	NVIDIA GEFORCE GTX 1050 TI	4.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:00:46+00	3a28190f-0d8c-4f33-9ee8-015f9b7e788f
unknown	gpu	NVIDIA GEFORCE RTX 3090	24.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	48.00	350.00	2026-07-22 18:00:46+00	bf375c38-cef9-4ba3-9a3c-751f58e1ea9c
unknown	gpu	NVIDIA GEFORCE RTX 3090 TI	24.00	\N	\N	0.460000	available	https://www.runpod.io/console/gpu-cloud	48.00	350.00	2026-07-22 18:00:46+00	4cc332a3-07f6-4c67-831c-483d5df43f79
unknown	gpu	NVIDIA GEFORCE RTX 4070 TI	12.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:00:46+00	152b7ce7-46fe-4019-b88e-517cf73b61b4
unknown	gpu	NVIDIA GEFORCE RTX 4080	16.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	320.00	2026-07-22 18:00:46+00	22a6f029-aa05-43b8-aad6-c85840c4830b
unknown	gpu	NVIDIA GEFORCE RTX 4080 SUPER	16.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	320.00	2026-07-22 18:00:46+00	ac3f551b-5c97-4a5e-bf29-baadb3ebe6a0
unknown	gpu	NVIDIA GEFORCE RTX 4090	24.00	\N	\N	0.690000	available	https://www.runpod.io/console/gpu-cloud	64.00	450.00	2026-07-22 18:00:46+00	34867c35-baeb-4d00-a9d9-c85cf90bcb89
unknown	gpu	NVIDIA GEFORCE RTX 5080	16.00	\N	\N	0.590000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:00:46+00	ab1824f4-ae78-4750-9012-d85e8d645431
unknown	gpu	NVIDIA GEFORCE RTX 5090	32.00	\N	\N	0.990000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:00:46+00	50ad425e-ae5c-4b98-975a-a66ad78af5ca
unknown	gpu	NVIDIA H100 80GB HBM3	80.00	\N	\N	2.990000	available	https://www.runpod.io/console/gpu-cloud	256.00	700.00	2026-07-22 18:00:46+00	bbb5b964-6beb-44ae-af8a-83fa0406a4fc
unknown	gpu	NVIDIA H100 NVL	94.00	\N	\N	3.190000	available	https://www.runpod.io/console/gpu-cloud	256.00	700.00	2026-07-22 18:00:46+00	9e7623be-1aaf-44e6-a61b-dfc3bb99a88c
unknown	gpu	NVIDIA H100 PCIE	80.00	\N	\N	2.890000	available	https://www.runpod.io/console/gpu-cloud	256.00	700.00	2026-07-22 18:00:46+00	7d7c2f07-5787-4253-8f5c-a96752854672
unknown	gpu	NVIDIA H200	141.00	\N	\N	4.390000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:00:46+00	2474a5e4-3d38-4746-992f-5fd6c40f6cc2
unknown	gpu	NVIDIA H200 NVL	143.00	\N	\N	3.790000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:00:46+00	3869d536-73c9-4400-a916-479ff2226283
unknown	gpu	NVIDIA L4	24.00	\N	\N	0.390000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:00:46+00	109a1004-d50f-4b79-836b-a22f57b11da4
unknown	gpu	NVIDIA L40	48.00	\N	\N	0.820000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:00:46+00	d100c3b8-d4ad-4e33-8d7c-1ecdeb0948e0
unknown	gpu	NVIDIA L40S	48.00	\N	\N	0.990000	available	https://www.runpod.io/console/gpu-cloud	128.00	350.00	2026-07-22 18:00:46+00	749d476b-8fbb-420a-b38e-1d8beccffe8c
unknown	gpu	NVIDIA RTX 2000 ADA GENERATION	16.00	\N	\N	0.240000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:00:46+00	5c370221-eeef-4113-9ba6-b031cf09fa81
unknown	gpu	NVIDIA RTX 4000 ADA GENERATION	20.00	\N	\N	0.280000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:00:46+00	e56ea10b-66db-48b7-af50-0694f76ef4c6
unknown	gpu	NVIDIA RTX 4000 SFF ADA GENERATION	20.00	\N	\N	0.440000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:00:46+00	e0986a83-70da-48f1-b8fe-56475fdfec29
unknown	gpu	NVIDIA RTX 5000 ADA GENERATION	32.00	\N	\N	0.830000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:00:46+00	f3d0890a-4a4d-4040-bf6d-15b607294660
unknown	gpu	NVIDIA RTX 6000 ADA GENERATION	48.00	\N	\N	0.840000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:00:46+00	96959b35-fa47-486f-9ad4-81a65d6b91ce
unknown	gpu	NVIDIA RTX A2000	6.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:00:46+00	08da6fe4-7fe9-4d84-876c-e8212b81544f
unknown	gpu	NVIDIA RTX A4000	16.00	\N	\N	0.250000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:00:46+00	c0ac5b57-771a-4800-9b5b-44811bb84898
unknown	gpu	NVIDIA RTX A4500	20.00	\N	\N	0.250000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:00:46+00	1574b318-df5e-49f4-8b80-9ede465bcec8
unknown	gpu	NVIDIA RTX A5000	24.00	\N	\N	0.270000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:00:46+00	8692603b-7945-40b3-a15c-e36da687b022
unknown	gpu	NVIDIA RTX A6000	48.00	\N	\N	0.530000	available	https://www.runpod.io/console/gpu-cloud	128.00	300.00	2026-07-22 18:00:46+00	6d84a1b3-7dd6-4d77-ab55-a5ed48680d42
unknown	gpu	NVIDIA RTX PRO 4000 BLACKWELL	24.00	\N	\N	0.570000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:00:46+00	8ff3ae67-5377-46d3-b97a-f427ef6ea184
unknown	gpu	NVIDIA RTX PRO 4500 BLACKWELL	32.00	\N	\N	0.740000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:00:46+00	0fbe196a-fb5c-4fe9-96d9-402a86d01c5b
unknown	gpu	NVIDIA RTX PRO 5000 BLACKWELL	48.00	\N	\N	0.960000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:00:46+00	7331273e-1146-4aac-9bc5-5837576f25d7
unknown	gpu	NVIDIA RTX PRO 6000 BLACKWELL MAX-Q WORKSTATION EDITION	96.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:00:46+00	e82ea782-f3be-47ee-be10-9321c9091657
unknown	gpu	NVIDIA RTX PRO 6000 BLACKWELL SERVER EDITION	96.00	\N	\N	1.990000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:00:46+00	aaf9daf7-bd02-431d-8d53-96cefe622a74
unknown	gpu	NVIDIA RTX PRO 6000 BLACKWELL SERVER EDITION MIG 1G.24GB	24.00	\N	\N	0.490000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:00:46+00	fffb4449-4619-46f9-90da-e3db80f4e125
unknown	gpu	NVIDIA RTX PRO 6000 BLACKWELL SERVER EDITION MIG 2G.48GB	48.00	\N	\N	1.000000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:00:46+00	ae67fb96-23b1-4b3e-b79b-67f89424288d
unknown	gpu	NVIDIA RTX PRO 6000 BLACKWELL WORKSTATION EDITION	96.00	\N	\N	1.890000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:00:46+00	5407eaa2-e20f-43ca-a6c1-4daccc73b63d
unknown	gpu	AMD INSTINCT MI300X OAM	192.00	\N	\N	2.390000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:01:10+00	66ee547b-0c1f-4abb-96c3-2f1fe0f6e7ee
unknown	gpu	NVIDIA A100 80GB PCIE	80.00	\N	\N	1.390000	available	https://www.runpod.io/console/gpu-cloud	128.00	400.00	2026-07-22 18:01:10+00	fa763601-00b5-44ed-8142-b7f714ab9af0
unknown	gpu	NVIDIA A100-SXM4-80GB	80.00	\N	\N	1.490000	available	https://www.runpod.io/console/gpu-cloud	128.00	400.00	2026-07-22 18:01:10+00	ce1f32da-7180-4587-9d28-bfbd648fa6d7
unknown	gpu	NVIDIA A40	48.00	\N	\N	0.440000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:01:10+00	1a7321d1-19a7-4e6b-a44e-25a7576efbdc
unknown	gpu	NVIDIA B200	180.00	\N	\N	5.890000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:01:10+00	fc858993-f537-4a4a-9938-91f73a486f88
unknown	gpu	NVIDIA B300 SXM6 AC	288.00	\N	\N	7.390000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:01:10+00	c9ae9d38-d7db-47ff-8880-3ca7178471e3
unknown	gpu	NVIDIA GEFORCE GTX 1050 TI	4.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:01:10+00	3052b269-79c2-43e6-99d1-32d31cf26ea5
unknown	gpu	NVIDIA GEFORCE RTX 3090	24.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	48.00	350.00	2026-07-22 18:01:10+00	ee1a0473-6ae9-4aca-aa56-1273240c09b7
unknown	gpu	NVIDIA GEFORCE RTX 3090 TI	24.00	\N	\N	0.460000	available	https://www.runpod.io/console/gpu-cloud	48.00	350.00	2026-07-22 18:01:10+00	12403fae-bcba-4a6e-a56f-3cae3a476591
unknown	gpu	NVIDIA GEFORCE RTX 4070 TI	12.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:01:10+00	e485a136-9cb5-4ee5-b025-c4bafaec985e
unknown	gpu	NVIDIA GEFORCE RTX 4080	16.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	320.00	2026-07-22 18:01:10+00	831be7de-3216-4388-85a5-2cf8de0e359a
unknown	gpu	NVIDIA GEFORCE RTX 4080 SUPER	16.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	320.00	2026-07-22 18:01:10+00	6b681fe6-8014-42cd-bd81-35ee7cb24662
unknown	gpu	NVIDIA GEFORCE RTX 4090	24.00	\N	\N	0.690000	available	https://www.runpod.io/console/gpu-cloud	64.00	450.00	2026-07-22 18:01:10+00	b526580c-416d-4a21-93a1-bcfd8e394d18
unknown	gpu	NVIDIA GEFORCE RTX 5080	16.00	\N	\N	0.590000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:01:10+00	9b8dfed6-d85d-48b5-baaa-2f0675b62576
unknown	gpu	NVIDIA GEFORCE RTX 5090	32.00	\N	\N	0.990000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:01:10+00	549d0ac8-4ab9-4184-8013-6d25be8f3484
unknown	gpu	NVIDIA H100 80GB HBM3	80.00	\N	\N	2.990000	available	https://www.runpod.io/console/gpu-cloud	256.00	700.00	2026-07-22 18:01:10+00	dad03f89-ae27-4047-89f7-6ca88562e2d0
unknown	gpu	NVIDIA H100 NVL	94.00	\N	\N	3.190000	available	https://www.runpod.io/console/gpu-cloud	256.00	700.00	2026-07-22 18:01:10+00	70843c66-2f1b-4716-97d7-e07821959afd
unknown	gpu	NVIDIA H100 PCIE	80.00	\N	\N	2.890000	available	https://www.runpod.io/console/gpu-cloud	256.00	700.00	2026-07-22 18:01:10+00	08fa5b07-6155-42b7-b9f2-492d9dd90146
unknown	gpu	NVIDIA H200	141.00	\N	\N	4.390000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:01:10+00	5ce10b79-eb9a-450d-a754-6f44eae423e8
unknown	gpu	NVIDIA H200 NVL	143.00	\N	\N	3.790000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:01:10+00	e131b0e9-13d4-4fea-9f5d-7ee372d406f5
unknown	gpu	NVIDIA L4	24.00	\N	\N	0.390000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:01:10+00	80e56583-0476-4385-b068-a2ac46d23373
unknown	gpu	NVIDIA L40	48.00	\N	\N	0.820000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:01:10+00	6f083b97-09eb-49f1-ac7f-e0419504a79d
unknown	gpu	NVIDIA L40S	48.00	\N	\N	0.990000	available	https://www.runpod.io/console/gpu-cloud	128.00	350.00	2026-07-22 18:01:10+00	6dbf725e-7938-478a-a18f-2c34a07db43b
unknown	gpu	NVIDIA RTX 2000 ADA GENERATION	16.00	\N	\N	0.240000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:01:10+00	de251790-44ae-4262-bc9d-4df8b08a371d
unknown	gpu	NVIDIA RTX 4000 ADA GENERATION	20.00	\N	\N	0.280000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:01:10+00	33727e0f-1042-4eea-9af7-6bbfee8a5317
unknown	gpu	NVIDIA RTX 4000 SFF ADA GENERATION	20.00	\N	\N	0.440000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:01:10+00	ed488560-38a6-4066-843c-e52736beee77
unknown	gpu	NVIDIA RTX 5000 ADA GENERATION	32.00	\N	\N	0.830000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:01:10+00	51a3058f-9557-48fe-9dd8-172463e94f6f
unknown	gpu	NVIDIA RTX 6000 ADA GENERATION	48.00	\N	\N	0.840000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:01:10+00	b0990160-60ee-4bf3-b2ea-8815148bc045
unknown	gpu	NVIDIA RTX A2000	6.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:01:10+00	5174301b-3c92-46fd-8bec-8157b7d7b6aa
unknown	gpu	NVIDIA RTX A4000	16.00	\N	\N	0.250000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:01:10+00	f48bd8f7-a366-40c3-8bf1-bdc90700220d
unknown	gpu	NVIDIA RTX A4500	20.00	\N	\N	0.250000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:01:10+00	33682b2e-4fdf-44ad-8dca-86759aa5b8fb
unknown	gpu	NVIDIA RTX A5000	24.00	\N	\N	0.270000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:01:10+00	a64057a0-4a0e-430e-9177-e67f6092b41e
unknown	gpu	NVIDIA RTX A6000	48.00	\N	\N	0.530000	available	https://www.runpod.io/console/gpu-cloud	128.00	300.00	2026-07-22 18:01:10+00	51281894-07bc-4820-a80c-4ea7ed2b5f3f
unknown	gpu	NVIDIA RTX PRO 4000 BLACKWELL	24.00	\N	\N	0.570000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:01:10+00	3f9cf254-afac-4b98-8500-466a4b53606e
unknown	gpu	NVIDIA RTX PRO 4500 BLACKWELL	32.00	\N	\N	0.740000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:01:10+00	87e486a8-02ff-412d-a515-5a859f83753a
unknown	gpu	NVIDIA RTX PRO 5000 BLACKWELL	48.00	\N	\N	0.960000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:01:10+00	54fa7e55-71eb-4d57-ac27-2608d080f4e4
unknown	gpu	NVIDIA RTX PRO 6000 BLACKWELL MAX-Q WORKSTATION EDITION	96.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:01:10+00	9f4c5ac4-fb07-44b0-b41e-89b317081796
unknown	gpu	NVIDIA RTX PRO 6000 BLACKWELL SERVER EDITION	96.00	\N	\N	1.990000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:01:10+00	ae239388-e368-4ad9-b678-725d76031457
unknown	gpu	NVIDIA RTX PRO 6000 BLACKWELL SERVER EDITION MIG 1G.24GB	24.00	\N	\N	0.490000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:01:10+00	8c10ed51-a47b-42cd-84f4-34cf2ac63aa7
unknown	gpu	NVIDIA RTX PRO 6000 BLACKWELL SERVER EDITION MIG 2G.48GB	48.00	\N	\N	1.000000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:01:10+00	17b69f34-923a-453d-8230-5566c5bc7499
unknown	gpu	NVIDIA RTX PRO 6000 BLACKWELL WORKSTATION EDITION	96.00	\N	\N	1.890000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 18:01:10+00	cad5e015-a828-4d14-a49c-e311bff66c43
unknown	gpu	AMD INSTINCT MI300X OAM	192.00	\N	\N	2.390000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:09:22+00	71c6e03b-62b0-448d-9d55-445be1bcac72
unknown	gpu	NVIDIA A100 80GB PCIE	80.00	\N	\N	1.390000	available	https://www.runpod.io/console/gpu-cloud	128.00	400.00	2026-07-22 19:09:22+00	c5f4520c-14e6-4c6b-863f-e188333ee360
unknown	gpu	NVIDIA A100-SXM4-80GB	80.00	\N	\N	1.490000	available	https://www.runpod.io/console/gpu-cloud	128.00	400.00	2026-07-22 19:09:22+00	5e891d5d-3943-4c8f-aab1-1235ce0d8c78
unknown	gpu	NVIDIA A40	48.00	\N	\N	0.440000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:09:22+00	97affcf9-eed6-47e2-85d5-e0ea9499fa50
unknown	gpu	NVIDIA B200	180.00	\N	\N	5.890000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:09:22+00	782eeb5d-a23a-4897-949a-cd13f3a4cce1
unknown	gpu	NVIDIA B300 SXM6 AC	288.00	\N	\N	7.390000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:09:22+00	73d589ba-3dba-4a6e-9e3d-47586a5891a5
unknown	gpu	NVIDIA GEFORCE GTX 1050 TI	4.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:09:22+00	afb95a51-c650-4dce-be31-3e6e3b4dfd65
unknown	gpu	NVIDIA GEFORCE RTX 3090	24.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	48.00	350.00	2026-07-22 19:09:22+00	8d9aaa40-9209-49c8-845c-a5928d4b58b3
unknown	gpu	NVIDIA GEFORCE RTX 3090 TI	24.00	\N	\N	0.460000	available	https://www.runpod.io/console/gpu-cloud	48.00	350.00	2026-07-22 19:09:22+00	164ee74a-7a4d-42fe-9ef5-34f434a302a5
unknown	gpu	NVIDIA GEFORCE RTX 4070 TI	12.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:09:22+00	a5f6ff08-7bb5-4512-b99a-d1b37efdfe18
unknown	gpu	NVIDIA GEFORCE RTX 4080	16.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	320.00	2026-07-22 19:09:22+00	71456376-df28-4675-ac92-e3f212f96bf2
unknown	gpu	NVIDIA GEFORCE RTX 4080 SUPER	16.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	320.00	2026-07-22 19:09:22+00	be245788-d485-4783-9a48-1f426faa8e48
unknown	gpu	NVIDIA GEFORCE RTX 4090	24.00	\N	\N	0.690000	available	https://www.runpod.io/console/gpu-cloud	64.00	450.00	2026-07-22 19:09:22+00	b1eaeb52-9a07-403f-b533-802aabe226cc
unknown	gpu	NVIDIA GEFORCE RTX 5080	16.00	\N	\N	0.590000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:09:22+00	4b8c012f-a38b-4538-83b6-0f69a6084f33
unknown	gpu	NVIDIA GEFORCE RTX 5090	32.00	\N	\N	0.990000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:09:22+00	5bb19c1a-2088-4c8b-a4fd-d6f4a83315b1
unknown	gpu	NVIDIA H100 80GB HBM3	80.00	\N	\N	2.990000	available	https://www.runpod.io/console/gpu-cloud	256.00	700.00	2026-07-22 19:09:22+00	dd54cf8e-589c-4d2d-8466-7049e15f4ad8
unknown	gpu	NVIDIA H100 NVL	94.00	\N	\N	3.190000	available	https://www.runpod.io/console/gpu-cloud	256.00	700.00	2026-07-22 19:09:22+00	cdb93be0-e514-438d-9cdd-31dcbff13dcf
unknown	gpu	NVIDIA H100 PCIE	80.00	\N	\N	2.890000	available	https://www.runpod.io/console/gpu-cloud	256.00	700.00	2026-07-22 19:09:22+00	8e6f32d5-07e3-48a8-a538-553ca86eef74
unknown	gpu	NVIDIA H200	141.00	\N	\N	4.390000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:09:22+00	bc0a7765-6e4b-441a-ae50-106c845e828c
unknown	gpu	NVIDIA H200 NVL	143.00	\N	\N	3.790000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:09:22+00	d69b7d8d-ec9d-4011-8ae9-45becaf2ff99
unknown	gpu	NVIDIA L4	24.00	\N	\N	0.390000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:09:22+00	81fe10e7-c0b4-4723-adbb-f1f0f15bd66c
unknown	gpu	NVIDIA L40	48.00	\N	\N	0.820000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:09:22+00	055d82dc-3012-4698-9d37-8e367b627fe4
unknown	gpu	NVIDIA L40S	48.00	\N	\N	0.990000	available	https://www.runpod.io/console/gpu-cloud	128.00	350.00	2026-07-22 19:09:22+00	e9b6303a-e7a4-470f-adf2-d46a5d84684a
unknown	gpu	NVIDIA RTX 2000 ADA GENERATION	16.00	\N	\N	0.240000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:09:22+00	f1c6a1c4-9fe9-49c9-9e66-809b657ca9c5
unknown	gpu	NVIDIA RTX 4000 ADA GENERATION	20.00	\N	\N	0.280000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:09:22+00	9ac97086-01e1-4840-b009-6165eb18dd0a
unknown	gpu	NVIDIA RTX 4000 SFF ADA GENERATION	20.00	\N	\N	0.440000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:09:22+00	c8b579a7-153f-4235-9c61-e6132cf43213
unknown	gpu	NVIDIA RTX 5000 ADA GENERATION	32.00	\N	\N	0.830000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:09:22+00	d8408d6a-ea16-4993-a525-e3770786318a
unknown	gpu	NVIDIA RTX 6000 ADA GENERATION	48.00	\N	\N	0.840000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:09:22+00	cf049d86-4c8c-404f-94f1-1fbfdff6bd96
unknown	gpu	NVIDIA RTX A2000	6.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:09:22+00	dddeaa12-56f5-4181-8cdf-494321aa1eaa
unknown	gpu	NVIDIA RTX A4000	16.00	\N	\N	0.250000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:09:22+00	a046798a-ffa4-47b6-87f8-4eeebb44233b
unknown	gpu	NVIDIA RTX A4500	20.00	\N	\N	0.250000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:09:22+00	ff6304d9-988d-44c0-be3f-2c322e6f6da1
unknown	gpu	NVIDIA RTX A5000	24.00	\N	\N	0.270000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:09:22+00	e0bac5b9-7dc6-4c1c-9ae7-8cfd78bac9e1
unknown	gpu	NVIDIA RTX A6000	48.00	\N	\N	0.530000	available	https://www.runpod.io/console/gpu-cloud	128.00	300.00	2026-07-22 19:09:22+00	6f3a56a7-029f-4bca-9598-2b00968ca262
unknown	gpu	NVIDIA RTX PRO 4000 BLACKWELL	24.00	\N	\N	0.570000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:09:22+00	cd2938e0-eae3-48b5-b51b-9895d161eb4f
unknown	gpu	NVIDIA RTX PRO 4500 BLACKWELL	32.00	\N	\N	0.740000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:09:22+00	8d282627-4312-4c70-a879-5c24cbd02355
unknown	gpu	NVIDIA RTX PRO 5000 BLACKWELL	48.00	\N	\N	0.960000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:09:22+00	44612bc9-a14b-4a93-b9ae-7d30b79f38cb
unknown	gpu	NVIDIA RTX PRO 6000 BLACKWELL MAX-Q WORKSTATION EDITION	96.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:09:22+00	d68a2463-efee-4854-8087-68549cb59683
unknown	gpu	NVIDIA RTX PRO 6000 BLACKWELL SERVER EDITION	96.00	\N	\N	1.990000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:09:22+00	f1145d12-d092-48a8-9d75-92ef848f606e
unknown	gpu	NVIDIA RTX PRO 6000 BLACKWELL SERVER EDITION MIG 1G.24GB	24.00	\N	\N	0.490000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:09:22+00	f94da1d3-91a6-462c-b362-ba3cece6d5d5
unknown	gpu	NVIDIA RTX PRO 6000 BLACKWELL SERVER EDITION MIG 2G.48GB	48.00	\N	\N	1.000000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:09:22+00	97d9ea39-d138-4627-b55e-a80177c3c9a3
unknown	gpu	NVIDIA RTX PRO 6000 BLACKWELL WORKSTATION EDITION	96.00	\N	\N	1.890000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:09:22+00	d5d6047d-ab0d-440a-ac9f-99e2123787cd
runpod	gpu	AMD INSTINCT MI300X OAM	192.00	\N	\N	2.390000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:19:15+00	bed31db9-46e6-4382-87b3-c56a42ce6468
runpod	gpu	NVIDIA A100 80GB PCIE	80.00	\N	\N	1.390000	available	https://www.runpod.io/console/gpu-cloud	128.00	400.00	2026-07-22 19:19:15+00	953726d2-e754-418c-8bbe-fde230dea6fc
runpod	gpu	NVIDIA A100-SXM4-80GB	80.00	\N	\N	1.490000	available	https://www.runpod.io/console/gpu-cloud	128.00	400.00	2026-07-22 19:19:15+00	fe1d1c9b-0e23-4d9a-b68c-9854beabc05a
runpod	gpu	NVIDIA A40	48.00	\N	\N	0.440000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:19:15+00	b20376f2-684a-4d66-8e88-56126b06f7d1
runpod	gpu	NVIDIA B200	180.00	\N	\N	5.890000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:19:15+00	9d7bed31-933b-49e5-a665-e440209b5ed3
runpod	gpu	NVIDIA B300 SXM6 AC	288.00	\N	\N	7.390000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:19:15+00	e5ee4313-8f58-4a84-9703-8917a62344bc
runpod	gpu	NVIDIA GEFORCE GTX 1050 TI	4.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:19:15+00	fb404e83-6a48-4b95-9faf-58addb481dd4
runpod	gpu	NVIDIA GEFORCE RTX 3090	24.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	48.00	350.00	2026-07-22 19:19:15+00	72464902-b796-4949-95bf-13f370fe3898
runpod	gpu	NVIDIA GEFORCE RTX 3090 TI	24.00	\N	\N	0.460000	available	https://www.runpod.io/console/gpu-cloud	48.00	350.00	2026-07-22 19:19:15+00	d29acdb1-f99d-425c-939b-b157592b86bb
runpod	gpu	NVIDIA GEFORCE RTX 4070 TI	12.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:19:15+00	0a8aaaa8-d174-472f-ba23-2914c33e370b
runpod	gpu	NVIDIA GEFORCE RTX 4080	16.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	320.00	2026-07-22 19:19:15+00	9956d29c-a5d4-4b98-b41b-6d40461265a2
runpod	gpu	NVIDIA GEFORCE RTX 4080 SUPER	16.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	320.00	2026-07-22 19:19:15+00	112321ed-4867-4ada-a068-828fa2ff491d
runpod	gpu	NVIDIA GEFORCE RTX 4090	24.00	\N	\N	0.690000	available	https://www.runpod.io/console/gpu-cloud	64.00	450.00	2026-07-22 19:19:15+00	5b2cf491-8772-4051-9c41-fac5b96b15a1
runpod	gpu	NVIDIA GEFORCE RTX 5080	16.00	\N	\N	0.590000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:19:15+00	a3b2db42-f4d5-4f5f-ac9d-92065609844b
runpod	gpu	NVIDIA GEFORCE RTX 5090	32.00	\N	\N	0.990000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:19:15+00	f298180e-1149-4ba2-b62f-c910d071ebcf
runpod	gpu	NVIDIA H100 80GB HBM3	80.00	\N	\N	2.990000	available	https://www.runpod.io/console/gpu-cloud	256.00	700.00	2026-07-22 19:19:15+00	b2322434-193e-4e3c-b06c-ea6cbeec79c3
runpod	gpu	NVIDIA H100 NVL	94.00	\N	\N	3.190000	available	https://www.runpod.io/console/gpu-cloud	256.00	700.00	2026-07-22 19:19:15+00	ebeb1859-cd7c-49cf-9087-ddfff820bc51
runpod	gpu	NVIDIA H100 PCIE	80.00	\N	\N	2.890000	available	https://www.runpod.io/console/gpu-cloud	256.00	700.00	2026-07-22 19:19:15+00	e7813c25-fdab-482b-9028-d13d7916ecc5
runpod	gpu	NVIDIA H200	141.00	\N	\N	4.390000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:19:15+00	fad46e65-0222-4eb6-8c47-cdafde2bb250
runpod	gpu	NVIDIA H200 NVL	143.00	\N	\N	3.790000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:19:15+00	5c68f05c-0117-48ee-b26b-4e9fcad27e8e
runpod	gpu	NVIDIA L4	24.00	\N	\N	0.390000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:19:15+00	b39b31ca-121f-4f80-9307-c640bb1a3e96
runpod	gpu	NVIDIA L40	48.00	\N	\N	0.820000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:19:15+00	9e7afc5a-86f7-4634-afae-fb1b179ba0ec
runpod	gpu	NVIDIA L40S	48.00	\N	\N	0.990000	available	https://www.runpod.io/console/gpu-cloud	128.00	350.00	2026-07-22 19:19:15+00	bbc751dd-0b0b-48a2-92c8-9fa430b0964f
runpod	gpu	NVIDIA RTX 2000 ADA GENERATION	16.00	\N	\N	0.240000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:19:15+00	31cfccbf-e8e7-4e2f-b28f-dae16246418b
runpod	gpu	NVIDIA RTX 4000 ADA GENERATION	20.00	\N	\N	0.280000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:19:15+00	3cb5c15a-3c1f-4076-9fc7-af93362c8767
runpod	gpu	NVIDIA RTX 4000 SFF ADA GENERATION	20.00	\N	\N	0.440000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:19:15+00	da752d15-0158-4766-8461-a3ec461795a5
runpod	gpu	NVIDIA RTX 5000 ADA GENERATION	32.00	\N	\N	0.830000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:19:15+00	f81a0c26-5965-4b6c-8247-fcd3f7b1fd81
runpod	gpu	NVIDIA RTX 6000 ADA GENERATION	48.00	\N	\N	0.840000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:19:15+00	3e72224c-2f3b-477d-b010-a319784f31da
runpod	gpu	NVIDIA RTX A2000	6.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:19:15+00	e83825ce-bd89-4cd5-a217-5652a4b9ec2d
runpod	gpu	NVIDIA RTX A4000	16.00	\N	\N	0.250000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:19:15+00	86d6d2d5-ae02-4b6c-9b4d-e49c8ce07507
runpod	gpu	NVIDIA RTX A4500	20.00	\N	\N	0.250000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:19:15+00	97a49e2c-90b0-4e0e-806a-4a847ed44022
runpod	gpu	NVIDIA RTX A5000	24.00	\N	\N	0.270000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:19:15+00	543f13b3-f934-48cc-beb0-46b72d6ea19f
runpod	gpu	NVIDIA RTX A6000	48.00	\N	\N	0.530000	available	https://www.runpod.io/console/gpu-cloud	128.00	300.00	2026-07-22 19:19:15+00	97197167-b831-425b-9671-f0a48d28e78c
runpod	gpu	NVIDIA RTX PRO 4000 BLACKWELL	24.00	\N	\N	0.570000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:19:15+00	c24a5dd1-2a83-498b-8c3f-06cb88ae036d
runpod	gpu	NVIDIA RTX PRO 4500 BLACKWELL	32.00	\N	\N	0.740000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:19:15+00	ff5e3902-2d35-4e1a-8d49-ae11878ec867
runpod	gpu	NVIDIA RTX PRO 5000 BLACKWELL	48.00	\N	\N	0.960000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:19:15+00	7498461d-9270-43bc-be5e-acdd8edc5d64
runpod	gpu	NVIDIA RTX PRO 6000 BLACKWELL MAX-Q WORKSTATION EDITION	96.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:19:15+00	9277a630-3d04-49df-b20a-3adb58e288cf
runpod	gpu	NVIDIA RTX PRO 6000 BLACKWELL SERVER EDITION	96.00	\N	\N	1.990000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:19:15+00	d71ea222-f47b-425f-a178-d94bbec545c8
runpod	gpu	NVIDIA RTX PRO 6000 BLACKWELL SERVER EDITION MIG 1G.24GB	24.00	\N	\N	0.490000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:19:15+00	8a06778e-d404-4247-bd37-13d047dd2ddd
runpod	gpu	NVIDIA RTX PRO 6000 BLACKWELL SERVER EDITION MIG 2G.48GB	48.00	\N	\N	1.000000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:19:15+00	77606294-c7b9-46cc-bd81-56eb3ae77424
runpod	gpu	NVIDIA RTX PRO 6000 BLACKWELL WORKSTATION EDITION	96.00	\N	\N	1.890000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:19:15+00	29d1eba1-bdeb-41ca-8006-362a8659111e
runpod	gpu	AMD INSTINCT MI300X OAM	192.00	\N	\N	2.390000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:33:46+00	4052cd42-5f4f-4c3c-89bb-3a1a901b1687
runpod	gpu	NVIDIA A100 80GB PCIE	80.00	\N	\N	1.390000	available	https://www.runpod.io/console/gpu-cloud	128.00	400.00	2026-07-22 19:33:46+00	7744c2cf-71ef-492c-891a-26ba3899adb4
runpod	gpu	NVIDIA A100-SXM4-80GB	80.00	\N	\N	1.490000	available	https://www.runpod.io/console/gpu-cloud	128.00	400.00	2026-07-22 19:33:46+00	9168a874-c756-43c4-8f0d-b1d0cc8cb9a8
runpod	gpu	NVIDIA A40	48.00	\N	\N	0.440000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:33:46+00	da6241e4-5f59-4b81-9757-c2ec6c876249
runpod	gpu	NVIDIA B200	180.00	\N	\N	5.890000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:33:46+00	b93ff4d1-a3a2-4249-9eb0-1f724aa89e81
runpod	gpu	NVIDIA B300 SXM6 AC	288.00	\N	\N	7.390000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:33:46+00	bec94da6-0e1a-4942-bd09-d16ac74260d5
runpod	gpu	NVIDIA GEFORCE GTX 1050 TI	4.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:33:46+00	5f4bdc7d-50dd-4819-b053-ad656f98e68b
runpod	gpu	NVIDIA GEFORCE RTX 3090	24.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	48.00	350.00	2026-07-22 19:33:46+00	4a5c007d-0f37-4d0c-959d-e2b168b85538
runpod	gpu	NVIDIA GEFORCE RTX 3090 TI	24.00	\N	\N	0.460000	available	https://www.runpod.io/console/gpu-cloud	48.00	350.00	2026-07-22 19:33:46+00	35e818cd-f70c-4208-8b5d-28dfcfd758bc
runpod	gpu	NVIDIA GEFORCE RTX 4070 TI	12.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:33:46+00	0d535eff-e5c6-4df3-a84b-024d084f2092
runpod	gpu	NVIDIA GEFORCE RTX 4080	16.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	320.00	2026-07-22 19:33:46+00	4c779803-0538-45ef-8346-b913b3976d28
runpod	gpu	NVIDIA GEFORCE RTX 4080 SUPER	16.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	320.00	2026-07-22 19:33:46+00	7a704c9d-a4de-45a0-9104-c61d87b99b4f
runpod	gpu	NVIDIA GEFORCE RTX 4090	24.00	\N	\N	0.690000	available	https://www.runpod.io/console/gpu-cloud	64.00	450.00	2026-07-22 19:33:46+00	e9813aff-a8e8-46dd-a192-225e2d9ee57a
runpod	gpu	NVIDIA GEFORCE RTX 5080	16.00	\N	\N	0.590000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:33:46+00	19275017-b624-4eca-b0a3-489bfe3199ea
runpod	gpu	NVIDIA GEFORCE RTX 5090	32.00	\N	\N	0.990000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:33:46+00	f37bb3a9-cefb-475c-8b3a-713d8e57c74c
runpod	gpu	NVIDIA H100 80GB HBM3	80.00	\N	\N	2.990000	available	https://www.runpod.io/console/gpu-cloud	256.00	700.00	2026-07-22 19:33:46+00	88737874-d646-4f2d-a3e1-f507633f9cbe
runpod	gpu	NVIDIA H100 NVL	94.00	\N	\N	3.190000	available	https://www.runpod.io/console/gpu-cloud	256.00	700.00	2026-07-22 19:33:46+00	6142ce74-d8cc-4814-8de6-21fbe684ef0e
runpod	gpu	NVIDIA H100 PCIE	80.00	\N	\N	2.890000	available	https://www.runpod.io/console/gpu-cloud	256.00	700.00	2026-07-22 19:33:46+00	aa425000-c5b6-483e-bf19-be4d73f6dced
runpod	gpu	NVIDIA H200	141.00	\N	\N	4.390000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:33:46+00	ea8a760b-6b08-438d-96c8-3e05ad9882e1
runpod	gpu	NVIDIA H200 NVL	143.00	\N	\N	3.790000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:33:46+00	564f955e-e80c-40d4-b008-d282a2db7237
runpod	gpu	NVIDIA L4	24.00	\N	\N	0.390000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:33:46+00	0b740c31-3c31-4459-a9aa-81dedba53b3a
runpod	gpu	NVIDIA L40	48.00	\N	\N	0.820000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:33:46+00	3c2a2e70-b1f4-4c4b-9da8-531b0aa6c027
runpod	gpu	NVIDIA L40S	48.00	\N	\N	0.990000	available	https://www.runpod.io/console/gpu-cloud	128.00	350.00	2026-07-22 19:33:46+00	3de760b7-cc5b-4956-8bd1-a97e059a0e68
runpod	gpu	NVIDIA RTX 2000 ADA GENERATION	16.00	\N	\N	0.240000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:33:46+00	38d8c592-6a14-4585-a5db-0549923bca6d
runpod	gpu	NVIDIA RTX 4000 ADA GENERATION	20.00	\N	\N	0.280000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:33:46+00	c1efef1d-ca58-45d7-aa38-fa5a9ad7fab5
runpod	gpu	NVIDIA RTX 4000 SFF ADA GENERATION	20.00	\N	\N	0.440000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:33:46+00	74042081-a969-4726-8fd3-2dc56321033c
runpod	gpu	NVIDIA RTX 5000 ADA GENERATION	32.00	\N	\N	0.830000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:33:46+00	baacbe83-d614-47be-8d6c-7274315a5bb7
runpod	gpu	NVIDIA RTX 6000 ADA GENERATION	48.00	\N	\N	0.840000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:33:46+00	5dec6715-db8c-456f-8df7-b435fb39ceaa
runpod	gpu	NVIDIA RTX A2000	6.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:33:46+00	bb64190b-4e6d-429f-ad0a-a7d36175d9c6
runpod	gpu	NVIDIA RTX A4000	16.00	\N	\N	0.250000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:33:46+00	a3c6e317-e02e-4e8b-9025-18552b55dde2
runpod	gpu	NVIDIA RTX A4500	20.00	\N	\N	0.250000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:33:46+00	5e294f29-893f-4831-825b-08cdb5b702c7
runpod	gpu	NVIDIA RTX A5000	24.00	\N	\N	0.270000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:33:46+00	c96638f1-f16a-4a8a-97ae-309c64d49925
unknown	gpu	RTX 5080	15.92	\N	\N	0.322222	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	e71a23ef-9da0-4e24-8a29-60816cb4aac6
runpod	gpu	NVIDIA RTX A6000	48.00	\N	\N	0.530000	available	https://www.runpod.io/console/gpu-cloud	128.00	300.00	2026-07-22 19:33:46+00	99d6bbd9-3453-4bd6-b076-256422c0c918
runpod	gpu	NVIDIA RTX PRO 4000 BLACKWELL	24.00	\N	\N	0.570000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:33:46+00	baba5a39-6f3c-4722-bd10-f084a97796da
runpod	gpu	NVIDIA RTX PRO 4500 BLACKWELL	32.00	\N	\N	0.740000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:33:46+00	047918c5-0031-4e8f-8ec2-d4c3e23f092d
runpod	gpu	NVIDIA RTX PRO 5000 BLACKWELL	48.00	\N	\N	0.960000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:33:46+00	d1583a69-b351-4e9b-a44f-1515a6a0aba3
runpod	gpu	NVIDIA RTX PRO 6000 BLACKWELL MAX-Q WORKSTATION EDITION	96.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:33:46+00	bfef7075-b7c7-46a4-8054-792eafc66150
runpod	gpu	NVIDIA RTX PRO 6000 BLACKWELL SERVER EDITION	96.00	\N	\N	1.990000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:33:46+00	41837971-7977-4cb2-a8bc-1b2ea3edb40a
runpod	gpu	NVIDIA RTX PRO 6000 BLACKWELL SERVER EDITION MIG 1G.24GB	24.00	\N	\N	0.490000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:33:46+00	3113a3b8-b0ed-407d-bb09-cda86706a9a9
runpod	gpu	NVIDIA RTX PRO 6000 BLACKWELL SERVER EDITION MIG 2G.48GB	48.00	\N	\N	1.000000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:33:46+00	7e75637f-27f7-40cd-b0c6-6c103216d444
runpod	gpu	NVIDIA RTX PRO 6000 BLACKWELL WORKSTATION EDITION	96.00	\N	\N	1.890000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-22 19:33:46+00	95306cc8-08d7-44cf-a3aa-5910d6b4fb75
runpod	gpu	AMD INSTINCT MI300X OAM	192.00	\N	\N	2.390000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:22:58+00	7f919b02-f992-468a-8fdc-1416d24f352a
runpod	gpu	NVIDIA A100 80GB PCIE	80.00	\N	\N	1.390000	available	https://www.runpod.io/console/gpu-cloud	128.00	400.00	2026-07-23 09:22:58+00	70e2715a-e876-4926-bbbb-78c86e950c49
runpod	gpu	NVIDIA A100-SXM4-80GB	80.00	\N	\N	1.490000	available	https://www.runpod.io/console/gpu-cloud	128.00	400.00	2026-07-23 09:22:58+00	1b14648c-a676-4c9d-96fb-da6213ed374f
runpod	gpu	NVIDIA A40	48.00	\N	\N	0.440000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:22:58+00	9b127947-ce37-40c0-b0bd-b86531056f0a
runpod	gpu	NVIDIA B200	180.00	\N	\N	5.890000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:22:58+00	062358e3-9ace-4bde-bd98-17355316724e
runpod	gpu	NVIDIA B300 SXM6 AC	288.00	\N	\N	7.390000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:22:58+00	072cb04b-2db1-4c17-928a-867ecf1e5799
runpod	gpu	NVIDIA GEFORCE GTX 1050 TI	4.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:22:58+00	01d643e3-8271-44e7-a8a0-f43877b6cbed
runpod	gpu	NVIDIA GEFORCE RTX 3090	24.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	48.00	350.00	2026-07-23 09:22:58+00	5bd07f2a-122c-4067-ba82-1bbbd8665f35
runpod	gpu	NVIDIA GEFORCE RTX 3090 TI	24.00	\N	\N	0.460000	available	https://www.runpod.io/console/gpu-cloud	48.00	350.00	2026-07-23 09:22:58+00	4228ef63-479f-44d9-bb01-fd13a65c08b1
runpod	gpu	NVIDIA GEFORCE RTX 4070 TI	12.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:22:58+00	c3cf701d-b21a-4931-8459-f9938962c9c9
runpod	gpu	NVIDIA GEFORCE RTX 4080	16.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	320.00	2026-07-23 09:22:58+00	16a69ac3-d00f-49af-87f9-32498a676de0
runpod	gpu	NVIDIA GEFORCE RTX 4080 SUPER	16.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	320.00	2026-07-23 09:22:58+00	3ae66e6f-3516-4b81-bbe6-fe052ef1acd6
runpod	gpu	NVIDIA GEFORCE RTX 4090	24.00	\N	\N	0.690000	available	https://www.runpod.io/console/gpu-cloud	64.00	450.00	2026-07-23 09:22:58+00	dd57618a-d1f7-41a0-adde-92b5226b2235
runpod	gpu	NVIDIA GEFORCE RTX 5080	16.00	\N	\N	0.590000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:22:58+00	577986a0-d2af-4f32-ab60-69f78bd05dab
runpod	gpu	NVIDIA GEFORCE RTX 5090	32.00	\N	\N	0.990000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:22:58+00	176c8117-bbcb-4a66-aca9-a2e0f23ee886
runpod	gpu	NVIDIA H100 80GB HBM3	80.00	\N	\N	2.990000	available	https://www.runpod.io/console/gpu-cloud	256.00	700.00	2026-07-23 09:22:58+00	f10bc33e-f70f-4d2d-b53a-05974038f772
runpod	gpu	NVIDIA H100 NVL	94.00	\N	\N	3.190000	available	https://www.runpod.io/console/gpu-cloud	256.00	700.00	2026-07-23 09:22:58+00	bf1eb45c-3604-4f8e-9d4e-d8758d50f8af
runpod	gpu	NVIDIA H100 PCIE	80.00	\N	\N	2.890000	available	https://www.runpod.io/console/gpu-cloud	256.00	700.00	2026-07-23 09:22:58+00	231f73f0-0074-44d9-b6c8-2353ce5cb7a0
runpod	gpu	NVIDIA H200	141.00	\N	\N	4.390000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:22:58+00	e62de065-3b84-407f-96df-d970cc449d2f
runpod	gpu	NVIDIA H200 NVL	143.00	\N	\N	3.790000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:22:58+00	09f2e847-e51a-48be-a1af-88d6eb202b0f
runpod	gpu	NVIDIA L4	24.00	\N	\N	0.390000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:22:58+00	ff5ff93f-ccd7-42c1-b58c-753388983bbd
runpod	gpu	NVIDIA L40	48.00	\N	\N	0.820000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:22:58+00	a46702b6-2b24-4435-a0d8-0be56399fbb3
runpod	gpu	NVIDIA L40S	48.00	\N	\N	0.990000	available	https://www.runpod.io/console/gpu-cloud	128.00	350.00	2026-07-23 09:22:58+00	06546e38-7e41-4aa1-b767-4462812532ce
runpod	gpu	NVIDIA RTX 2000 ADA GENERATION	16.00	\N	\N	0.240000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:22:58+00	136a4add-8c12-49e1-911b-40d8fbaf753d
runpod	gpu	NVIDIA RTX 4000 ADA GENERATION	20.00	\N	\N	0.280000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:22:58+00	2622d829-0d31-47e2-9424-a003f1831243
runpod	gpu	NVIDIA RTX 4000 SFF ADA GENERATION	20.00	\N	\N	0.440000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:22:58+00	824390d1-7c28-4c4b-8f3a-3df5e9e7927d
runpod	gpu	NVIDIA RTX 5000 ADA GENERATION	32.00	\N	\N	0.830000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:22:58+00	ec065568-732e-4606-bbb8-e511aab9f522
runpod	gpu	NVIDIA RTX 6000 ADA GENERATION	48.00	\N	\N	0.840000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:22:58+00	1e746075-f80b-4ebd-a430-e8f6229b8c71
runpod	gpu	NVIDIA RTX A2000	6.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:22:58+00	65541126-1450-438a-b610-932831e34740
runpod	gpu	NVIDIA RTX A4000	16.00	\N	\N	0.250000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:22:58+00	d06daf63-6707-446c-9707-a138c09f1184
runpod	gpu	NVIDIA RTX A4500	20.00	\N	\N	0.250000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:22:58+00	b6c41d2b-1a66-4e06-b0f4-ae2f66cab701
runpod	gpu	NVIDIA RTX A5000	24.00	\N	\N	0.270000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:22:58+00	adefe91b-fca8-4b5d-b103-0a7475ffd458
runpod	gpu	NVIDIA RTX A6000	48.00	\N	\N	0.530000	available	https://www.runpod.io/console/gpu-cloud	128.00	300.00	2026-07-23 09:22:58+00	e21b5336-8ba4-4750-8114-e7978a980ed1
runpod	gpu	NVIDIA RTX PRO 4000 BLACKWELL	24.00	\N	\N	0.570000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:22:58+00	753698df-18d2-4a0a-93d6-4ac1edaff17c
runpod	gpu	NVIDIA RTX PRO 4500 BLACKWELL	32.00	\N	\N	0.740000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:22:58+00	0a90965f-bee2-4bc0-970c-55a9ab6a93f3
runpod	gpu	NVIDIA RTX PRO 5000 BLACKWELL	48.00	\N	\N	0.960000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:22:58+00	c2d5b0f7-1a2b-4436-a84b-c5acd52ee775
runpod	gpu	NVIDIA RTX PRO 6000 BLACKWELL MAX-Q WORKSTATION EDITION	96.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:22:58+00	dfcded63-82ac-4f22-a8a2-30221c3f1239
runpod	gpu	NVIDIA RTX PRO 6000 BLACKWELL SERVER EDITION	96.00	\N	\N	1.990000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:22:58+00	e776dcbd-6cb8-40de-8622-188d7f50cd2e
runpod	gpu	NVIDIA RTX PRO 6000 BLACKWELL SERVER EDITION MIG 1G.24GB	24.00	\N	\N	0.490000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:22:58+00	6b357500-5472-4a45-879c-c0651b1d403d
runpod	gpu	NVIDIA RTX PRO 6000 BLACKWELL SERVER EDITION MIG 2G.48GB	48.00	\N	\N	1.000000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:22:58+00	47a2f32a-4028-4cc9-aaed-c0e9e1d44acd
runpod	gpu	NVIDIA RTX PRO 6000 BLACKWELL WORKSTATION EDITION	96.00	\N	\N	1.890000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:22:58+00	c8099ec8-c8ed-4170-87c5-dcfb6bacf14e
runpod	gpu	AMD INSTINCT MI300X OAM	192.00	\N	\N	2.390000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:30:57+00	13e5577a-a41e-4d88-a8e3-98227f9036fd
runpod	gpu	NVIDIA A100 80GB PCIE	80.00	\N	\N	1.390000	available	https://www.runpod.io/console/gpu-cloud	128.00	400.00	2026-07-23 09:30:57+00	87ce49d6-cbc7-4a60-9760-478148e64226
runpod	gpu	NVIDIA A100-SXM4-80GB	80.00	\N	\N	1.490000	available	https://www.runpod.io/console/gpu-cloud	128.00	400.00	2026-07-23 09:30:57+00	eeb5a2f2-4876-46fe-93f1-bad67eba390a
runpod	gpu	NVIDIA A40	48.00	\N	\N	0.440000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:30:57+00	5a9a49b5-97f5-436d-9416-e324ce860844
runpod	gpu	NVIDIA B200	180.00	\N	\N	5.890000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:30:57+00	6033f117-f85d-47a0-aef5-11b38c92c1a1
runpod	gpu	NVIDIA B300 SXM6 AC	288.00	\N	\N	7.390000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:30:57+00	050ea90b-0228-4f3e-9e84-f2a4828ea841
runpod	gpu	NVIDIA GEFORCE GTX 1050 TI	4.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:30:57+00	9eec754f-725f-434b-8100-35eb8ad691e5
runpod	gpu	NVIDIA GEFORCE RTX 3090	24.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	48.00	350.00	2026-07-23 09:30:57+00	039f12b2-9a13-49d2-b137-cc6a61d1fab4
runpod	gpu	NVIDIA GEFORCE RTX 3090 TI	24.00	\N	\N	0.460000	available	https://www.runpod.io/console/gpu-cloud	48.00	350.00	2026-07-23 09:30:57+00	3feead10-e1e8-4beb-9d83-952aaca03c74
runpod	gpu	NVIDIA GEFORCE RTX 4070 TI	12.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:30:57+00	483d412e-17db-408a-80a5-0f93b638de97
runpod	gpu	NVIDIA GEFORCE RTX 4080	16.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	320.00	2026-07-23 09:30:57+00	b0ce6719-7b3e-46ee-b9ed-8c37e65a0ffa
runpod	gpu	NVIDIA GEFORCE RTX 4080 SUPER	16.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	320.00	2026-07-23 09:30:57+00	030aa350-7812-413f-93d1-5b8ebc76d840
runpod	gpu	NVIDIA GEFORCE RTX 4090	24.00	\N	\N	0.690000	available	https://www.runpod.io/console/gpu-cloud	64.00	450.00	2026-07-23 09:30:57+00	7973bf4f-b4f4-42c9-9ec2-a1d5297d7448
runpod	gpu	NVIDIA GEFORCE RTX 5080	16.00	\N	\N	0.590000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:30:57+00	07360075-4803-468b-a451-694e717667e2
runpod	gpu	NVIDIA GEFORCE RTX 5090	32.00	\N	\N	0.990000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:30:57+00	e95c7222-c1aa-41d5-8dae-114e06345bf5
runpod	gpu	NVIDIA H100 80GB HBM3	80.00	\N	\N	2.990000	available	https://www.runpod.io/console/gpu-cloud	256.00	700.00	2026-07-23 09:30:57+00	2b1f3c35-bd1e-4410-9340-a1ed2f60117e
runpod	gpu	NVIDIA H100 NVL	94.00	\N	\N	3.190000	available	https://www.runpod.io/console/gpu-cloud	256.00	700.00	2026-07-23 09:30:57+00	ab755dd6-d097-44aa-8121-681211839e41
runpod	gpu	NVIDIA H100 PCIE	80.00	\N	\N	2.890000	available	https://www.runpod.io/console/gpu-cloud	256.00	700.00	2026-07-23 09:30:57+00	50c61b2f-cf34-4208-bdd4-9e14cb4a4b99
runpod	gpu	NVIDIA H200	141.00	\N	\N	4.390000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:30:57+00	07e8594a-3d0d-4eee-b5ea-4176046d28ba
runpod	gpu	NVIDIA H200 NVL	143.00	\N	\N	3.790000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:30:57+00	7b36e8eb-ef38-4fda-991e-76fc0c780bca
runpod	gpu	NVIDIA L4	24.00	\N	\N	0.390000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:30:57+00	fda96c79-6713-4e38-be34-8d4ed00bbd77
runpod	gpu	NVIDIA L40	48.00	\N	\N	0.820000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:30:57+00	03118222-bd6a-4fe2-a36f-b3b334b400ed
runpod	gpu	NVIDIA L40S	48.00	\N	\N	0.990000	available	https://www.runpod.io/console/gpu-cloud	128.00	350.00	2026-07-23 09:30:57+00	37bf823f-93ce-469f-a4b6-2798d0ad9f93
runpod	gpu	NVIDIA RTX 2000 ADA GENERATION	16.00	\N	\N	0.240000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:30:57+00	c5b037ed-bb2d-4ca1-b0bc-147b19858ccc
runpod	gpu	NVIDIA RTX 4000 ADA GENERATION	20.00	\N	\N	0.280000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:30:57+00	3abc3c81-d5d9-4c3d-ab9a-9bb1df9fb2cf
runpod	gpu	NVIDIA RTX 4000 SFF ADA GENERATION	20.00	\N	\N	0.440000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:30:57+00	da8c61bf-65ba-4d60-98a3-8d5845c088de
runpod	gpu	NVIDIA RTX 5000 ADA GENERATION	32.00	\N	\N	0.830000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:30:57+00	6b672692-1523-40c1-91f8-2a572bb1f61a
runpod	gpu	NVIDIA RTX 6000 ADA GENERATION	48.00	\N	\N	0.840000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:30:57+00	4dbb3ab7-ebba-4a7e-b04f-a48d75261be4
runpod	gpu	NVIDIA RTX A2000	6.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:30:57+00	a862297e-e785-4eb6-958b-5f3184374b99
runpod	gpu	NVIDIA RTX A4000	16.00	\N	\N	0.250000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:30:57+00	1ce84331-0f77-49dc-a6dd-82cb3a00980b
runpod	gpu	NVIDIA RTX A4500	20.00	\N	\N	0.250000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:30:57+00	5936c036-71a7-49f0-b5a0-d1dc075f3018
runpod	gpu	NVIDIA RTX A5000	24.00	\N	\N	0.270000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:30:57+00	0a65ac31-486f-44ad-87cd-fd2cbbf3d4e6
runpod	gpu	NVIDIA RTX A6000	48.00	\N	\N	0.530000	available	https://www.runpod.io/console/gpu-cloud	128.00	300.00	2026-07-23 09:30:57+00	2835b604-2051-4aa6-b6a4-d2d45cf4fceb
runpod	gpu	NVIDIA RTX PRO 4000 BLACKWELL	24.00	\N	\N	0.570000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:30:57+00	e3f57925-3337-4e91-bd16-45b78e651f1c
runpod	gpu	NVIDIA RTX PRO 4500 BLACKWELL	32.00	\N	\N	0.740000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:30:57+00	c0e64a9f-d967-403e-a559-72dc83a2c9ab
runpod	gpu	NVIDIA RTX PRO 5000 BLACKWELL	48.00	\N	\N	0.960000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:30:57+00	59473cb8-008a-4f16-821c-9dd13ccfb6aa
runpod	gpu	NVIDIA RTX PRO 6000 BLACKWELL MAX-Q WORKSTATION EDITION	96.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:30:57+00	8058bc9d-4d18-4272-acc1-920557e7615f
runpod	gpu	NVIDIA RTX PRO 6000 BLACKWELL SERVER EDITION	96.00	\N	\N	1.990000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:30:57+00	cdefd2a5-d2ac-4417-ba16-082658536ea5
runpod	gpu	NVIDIA RTX PRO 6000 BLACKWELL SERVER EDITION MIG 1G.24GB	24.00	\N	\N	0.490000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:30:57+00	15cb18a8-a964-4f30-99f8-477853c83e66
runpod	gpu	NVIDIA RTX PRO 6000 BLACKWELL SERVER EDITION MIG 2G.48GB	48.00	\N	\N	1.000000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:30:57+00	20607621-b1d5-4bc7-ab65-2128d3676f2f
runpod	gpu	NVIDIA RTX PRO 6000 BLACKWELL WORKSTATION EDITION	96.00	\N	\N	1.890000	available	https://www.runpod.io/console/gpu-cloud	32.00	250.00	2026-07-23 09:30:57+00	608bd5ae-b6c0-46fe-bb6a-5fb9a3ff3045
unknown	gpu	H100	80.00	\N	\N	2.400000	available	https://console.runyour.ai/gpu-cloud	256.00	700.00	2026-07-22 18:01:12+00	e275fc88-ce1e-4383-83db-8445508ebe0e
unknown	gpu	A100	80.00	\N	\N	1.600000	available	https://console.runyour.ai/gpu-cloud	128.00	400.00	2026-07-22 18:01:12+00	3826d8ab-b559-4ab5-921c-b18b1ae867db
unknown	gpu	RTX 4090	24.00	\N	\N	0.350000	available	https://console.runyour.ai/gpu-cloud	64.00	450.00	2026-07-22 18:01:12+00	fb39ed5d-9eca-4765-8929-6cccd13af288
unknown	gpu	H100	80.00	\N	\N	2.400000	available	https://console.runyour.ai/gpu-cloud	256.00	700.00	2026-07-22 19:09:24+00	b9ccb971-91af-4684-8403-a761191cf812
unknown	gpu	A100	80.00	\N	\N	1.600000	available	https://console.runyour.ai/gpu-cloud	128.00	400.00	2026-07-22 19:09:24+00	b78b176c-ed9e-4599-82eb-1d87a46e4913
unknown	gpu	RTX 4090	24.00	\N	\N	0.350000	available	https://console.runyour.ai/gpu-cloud	64.00	450.00	2026-07-22 19:09:24+00	e6069c57-3e1a-4eea-96c9-0f958b706c4e
runyourai	gpu	H100	80.00	\N	\N	2.400000	available	https://console.runyour.ai/gpu-cloud	256.00	700.00	2026-07-22 19:19:17+00	004bbf4b-f808-4418-9003-32f616bd4e7b
runyourai	gpu	A100	80.00	\N	\N	1.600000	available	https://console.runyour.ai/gpu-cloud	128.00	400.00	2026-07-22 19:19:17+00	72c47eca-cf45-4962-88bd-b625a96401aa
runyourai	gpu	RTX 4090	24.00	\N	\N	0.350000	available	https://console.runyour.ai/gpu-cloud	64.00	450.00	2026-07-22 19:19:17+00	34ac93db-e861-4266-9105-805ffd8314c5
runyourai	gpu	H100	80.00	\N	\N	2.400000	available	https://console.runyour.ai/gpu-cloud	256.00	700.00	2026-07-22 19:33:47+00	383cddd9-f8bb-491d-83d8-5466359dbf58
runyourai	gpu	A100	80.00	\N	\N	1.600000	available	https://console.runyour.ai/gpu-cloud	128.00	400.00	2026-07-22 19:33:47+00	04d99c35-3614-4169-98f5-145c3227948d
runyourai	gpu	RTX 4090	24.00	\N	\N	0.350000	available	https://console.runyour.ai/gpu-cloud	64.00	450.00	2026-07-22 19:33:47+00	8285fa32-475a-4624-bbd5-a9a8219bf635
runyourai	gpu	H100	80.00	\N	\N	2.400000	available	https://console.runyour.ai/gpu-cloud	256.00	700.00	2026-07-23 09:23:34+00	1ae01dd8-e600-4dd7-aa5b-eca7086f3d76
runyourai	gpu	A100	80.00	\N	\N	1.600000	available	https://console.runyour.ai/gpu-cloud	128.00	400.00	2026-07-23 09:23:34+00	f080eed3-1d53-417f-8d55-7a6141167045
runyourai	gpu	RTX 4090	24.00	\N	\N	0.350000	available	https://console.runyour.ai/gpu-cloud	64.00	450.00	2026-07-23 09:23:34+00	e9a6a94d-070b-4a38-9d58-84de6765b642
runyourai	gpu	H100	80.00	\N	\N	2.400000	available	https://console.runyour.ai/gpu-cloud	256.00	700.00	2026-07-23 09:31:32+00	a9575a34-ac91-4ee2-9ca5-d1bf91227fd9
runyourai	gpu	A100	80.00	\N	\N	1.600000	available	https://console.runyour.ai/gpu-cloud	128.00	400.00	2026-07-23 09:31:32+00	8527c352-8c2b-449c-86a8-c6b1ebfc2e9e
runyourai	gpu	RTX 4090	24.00	\N	\N	0.350000	available	https://console.runyour.ai/gpu-cloud	64.00	450.00	2026-07-23 09:31:32+00	e157238c-e498-4849-b185-11709d84eab8
sugarcube	gpu	A100	80.00	\N	\N	1.700000	available	https://sugarcube.co.kr	128.00	400.00	2026-07-22 20:23:04+00	c0bd6a8b-65e5-4249-9f0e-cda62dd53baa
sugarcube	gpu	RTX 4090	24.00	\N	\N	0.400000	available	https://sugarcube.co.kr	64.00	450.00	2026-07-22 20:23:04+00	2d58a6c0-3705-4ea5-96cb-9ca391ca2386
sugarcube	gpu	A100 PCIE 80GB (서버형)	80.00	\N	\N	1.950000	available	https://sugarcube.co.kr	128.00	400.00	2026-07-22 20:25:24+00	40ecd6cc-2c5b-4d9f-b7b7-cd138ffe9cf9
sugarcube	gpu	RTX 4090 24GB (워크스테이션)	24.00	\N	\N	0.420000	available	https://sugarcube.co.kr	64.00	450.00	2026-07-22 20:25:24+00	06a4a95d-8043-4bd2-a55d-643439fdcba4
sugarcube	gpu	RTX 3090 24GB (워크스테이션)	24.00	\N	\N	0.280000	available	https://sugarcube.co.kr	48.00	350.00	2026-07-22 20:25:24+00	61d1c629-5ae9-482c-b145-a0e9fbe2e08b
unknown	gpu	RTX 5090	31.84	\N	\N	0.057778	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	cbc2c11b-35d0-4e8b-ac4e-5cb42519afe2
unknown	gpu	RTX 5090	31.84	\N	\N	0.111111	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	49a91ab3-3fb3-4e6a-87a4-7f9b9dbd8a5c
unknown	gpu	TESLA V100	32.00	\N	\N	0.087556	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	ac0bdb25-74c4-4bdc-a85b-4c7ba6af4f29
unknown	gpu	TESLA V100	32.00	\N	\N	0.162222	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	3aee6725-0190-4acc-afbe-9d4ec4947b6a
unknown	gpu	TESLA V100	32.00	\N	\N	0.020889	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	3bf42067-67cf-434c-9a87-70aa9dc0ee09
unknown	gpu	TESLA V100	32.00	\N	\N	0.044889	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	d38982fa-b166-4444-8b53-c6eb82032926
unknown	gpu	RTX 5090	31.84	\N	\N	0.294815	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	1d3f0631-bf09-4fac-b861-8583d88cf359
unknown	gpu	RTX 5090	31.84	\N	\N	0.911111	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	0c53b440-f6eb-451e-973c-d45c24653ae9
unknown	gpu	RTX 5070 TI	15.92	\N	\N	0.095556	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	cac97993-47f7-48f5-98f6-40bb09427bee
unknown	gpu	RTX 5090	31.84	\N	\N	0.457778	available	\N	\N	\N	2026-07-22 16:50:59+00	a3b3d61e-8bdd-4c20-80fa-0e69db7f5673
unknown	gpu	RTX PRO 6000 WS	95.59	\N	\N	0.934815	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	1fbdd08f-ac27-479d-be5c-000a3c1718f5
unknown	gpu	H100 NVL	93.58	\N	\N	1.334815	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	428c40b6-d813-4e92-ad36-d04a517b9afc
unknown	gpu	RTX PRO 6000 WS	95.59	\N	\N	2.135556	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	4c11f887-d213-4ecd-95ac-3fbd3b06f10b
unknown	gpu	RTX PRO 6000 WS	95.59	\N	\N	0.754074	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	433ac48f-3f43-4c00-bd8e-09d8798dcc02
unknown	gpu	RTX 4090	23.99	\N	\N	0.168889	available	\N	\N	\N	2026-07-22 16:50:59+00	6d218b48-6252-4429-b4dd-c511b7914a2e
unknown	gpu	RTX 5090	31.84	\N	\N	0.562222	available	\N	\N	\N	2026-07-22 16:50:59+00	c6c5cdd2-2ac0-45c8-95e7-94312aed4dc8
unknown	gpu	RTX 5090	31.84	\N	\N	0.897037	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	ecd9081c-bee6-4799-a41d-c408677950e7
unknown	gpu	RTX 4070S TI	15.99	\N	\N	0.080296	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	87b7113d-8797-40a4-814e-eb6fb3cfcb07
unknown	gpu	RTX 5090	31.84	\N	\N	0.281481	available	\N	\N	\N	2026-07-22 16:50:59+00	0327e316-142c-4cf3-881d-de73375a20fd
unknown	gpu	RTX 4090	23.99	\N	\N	0.135556	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	a48bf89d-2ac7-4eaf-8640-21e20537acd5
unknown	gpu	RTX PRO 6000 S	95.59	\N	\N	1.202222	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	2053f7f0-77be-42a5-be62-4ea50665f402
unknown	gpu	RTX 4090	23.99	\N	\N	0.268889	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	5116aa2f-2f62-48d9-b57c-ff6439e0cfaa
unknown	gpu	RTX 5070	11.94	\N	\N	0.217778	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	872a80d6-07e5-46e3-a758-fb144940f434
unknown	gpu	H100 SXM	79.65	\N	\N	1.468889	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	d705199f-bc2d-40ff-9fc3-ba7e14048ed2
unknown	gpu	RTX 4080S	15.99	\N	\N	0.098222	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	ac2cb2df-0043-4b13-9d49-b35754e66a13
unknown	gpu	RTX 5070	11.94	\N	\N	0.431111	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	abb40cb7-ea01-4396-a68d-1e66d0d432b1
unknown	gpu	RTX 5090	31.84	\N	\N	0.403704	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	4b66f200-819a-422a-b83c-ac0311509dd2
unknown	gpu	RTX 5070 TI	15.92	\N	\N	0.214815	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	67c4dd76-9cee-42e8-9b13-ba31dc436166
unknown	gpu	RTX 5070	11.94	\N	\N	0.111111	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	a20fa58e-9e80-4971-b319-bf9d954ee07a
unknown	gpu	RTX 4090	47.99	\N	\N	0.297037	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	4a10f744-04b7-45fb-8fa1-88a933408b79
unknown	gpu	RTX 4080S	15.99	\N	\N	0.098222	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	3bf02d68-58e8-4c53-b330-e30cc59f400f
unknown	gpu	H100 SXM	79.65	\N	\N	2.935556	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	e9e6acbb-597f-46fb-ba46-bf36496a51ac
unknown	gpu	RTX 5080	15.92	\N	\N	0.143452	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	16c207cd-12e7-4f12-9ea7-50c97cc1d5e8
unknown	gpu	RTX 5070	11.94	\N	\N	0.857778	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	22c886a0-841f-45c0-a8bb-c4c23c0b9bbd
unknown	gpu	RTX 4090	47.99	\N	\N	0.590370	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	1e6ccfde-ec1a-4567-8daa-ee9371e76dfa
unknown	gpu	RTX PRO 6000 WS	95.59	\N	\N	1.329037	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	5aa8f1ad-0cdd-4125-b49d-fb452ebde8e1
unknown	gpu	RTX 4090	23.99	\N	\N	0.535556	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	347d6a4d-c47f-4ce8-8b1e-78b2a7e58301
unknown	gpu	RTX 5090	31.84	\N	\N	1.607407	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	87879209-fcec-40ad-b273-6be5b97d4e9b
unknown	gpu	RTX 5070 TI	15.92	\N	\N	0.135556	available	\N	\N	\N	2026-07-22 16:50:59+00	d12a6b5c-ab7f-4b9b-9f09-8fe8273aac05
unknown	gpu	RTX 5090	31.84	\N	\N	0.470370	available	\N	\N	\N	2026-07-22 16:50:59+00	79f70311-1cac-467a-9461-6d2cf80ac7a2
unknown	gpu	L4	22.49	\N	\N	0.032593	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	8e0bd47e-138d-456c-8bc2-efd17d1fad16
unknown	gpu	RTX 5090	31.84	\N	\N	0.212889	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	a5c7c149-264b-4cc4-a871-6c88b526d30f
unknown	gpu	RTX PRO 6000 S	95.59	\N	\N	2.783704	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	89da7351-dbfb-4e3a-bb70-4e8ea6dc4518
unknown	gpu	RTX 4090	23.99	\N	\N	0.321407	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	2a45e4d4-e44d-497a-aac9-bf6d6fd14446
unknown	gpu	RTX PRO 6000 S	95.59	\N	\N	1.736296	available	\N	\N	\N	2026-07-22 16:50:59+00	4e62e6b3-4369-47a2-b594-426e95c5180a
unknown	gpu	RTX 5090	31.84	\N	\N	1.337037	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	cab3311d-547c-4a7f-8dc1-35bd08348cc5
unknown	gpu	RTX 5080	15.92	\N	\N	0.189630	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	bf9dfbeb-9617-4b65-8f43-75f9c25b4531
unknown	gpu	RTX 4090	47.99	\N	\N	0.935556	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	952e6e61-1ef6-4757-a5f6-2403ef8859f1
unknown	gpu	RTX PRO 5000	47.79	\N	\N	2.560074	available	\N	\N	\N	2026-07-22 16:50:59+00	2bd8b4f2-5075-4b4c-ab8c-1d93b60d5b10
unknown	gpu	RTX 5090	31.84	\N	\N	0.403704	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	04e0156d-5df7-439e-9ce7-4795cbcf6305
unknown	gpu	RTX 4090	47.99	\N	\N	0.468889	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	06e2f2b4-ca90-454f-b678-544bc8806704
unknown	gpu	RTX PRO 6000 S	95.59	\N	\N	3.469630	available	\N	\N	\N	2026-07-22 16:50:59+00	fbf2ba7f-97bd-4f95-a3a2-8f443e6b8eae
unknown	gpu	RTX 5090	31.84	\N	\N	2.454815	available	\N	\N	\N	2026-07-22 16:50:59+00	f2a25a37-54fa-42af-be2b-061c8e089c01
unknown	gpu	RTX PRO 5000	47.79	\N	\N	1.258519	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	d3d48977-18a5-4c83-89c2-0a4aea81932e
unknown	gpu	RTX 5090	31.84	\N	\N	3.631111	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	1cc2f819-59e2-4a5f-a4f3-205f8379fdb9
unknown	gpu	RTX 5060 TI	15.93	\N	\N	0.080593	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	ea0b3023-61f5-4a5a-acf5-e57eab4a94a5
unknown	gpu	RTX PRO 6000 WS	95.59	\N	\N	2.803704	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	20709309-55bf-48d7-ac64-a80ad674ce0e
unknown	gpu	RTX PRO 6000 S	95.59	\N	\N	3.469630	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	1b19b2d5-fd49-4056-b1a1-41c06e26d075
unknown	gpu	RTX 4090	23.99	\N	\N	0.337778	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	6b916e9b-6c38-4d43-aa0c-26bce910b8ea
unknown	gpu	RTX PRO 6000 S	95.59	\N	\N	1.736296	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	c99f9086-4177-4c73-8218-cc0fceb473d3
unknown	gpu	H200 NVL	140.40	\N	\N	2.610222	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	c8eb3ffd-df0f-4fad-9140-be757da4c9f1
unknown	gpu	RTX 4090D	23.99	\N	\N	0.388148	unavailable	\N	\N	\N	2026-07-22 16:50:59+00	d8520dbf-9983-4b0d-8114-3f870dbbf3e6
unknown	gpu	RTX 5090	31.84	\N	\N	0.057778	unavailable	https://console.vast.ai/console/create/	62.80	250.00	2026-07-22 17:52:56+00	f1e5797e-733f-4aa1-bea8-38bb0b68df98
unknown	gpu	RTX 5090	31.84	\N	\N	0.111111	unavailable	https://console.vast.ai/console/create/	125.60	250.00	2026-07-22 17:52:56+00	eee75574-43e0-478c-af85-7809995304f8
unknown	gpu	TESLA V100	32.00	\N	\N	0.151556	unavailable	https://console.vast.ai/console/create/	251.10	300.00	2026-07-22 17:52:56+00	a426dc31-7472-4823-8700-ba00dcc667e1
unknown	gpu	TESLA V100	32.00	\N	\N	0.076889	unavailable	https://console.vast.ai/console/create/	125.50	300.00	2026-07-22 17:52:56+00	309a66df-586e-4896-8d66-b98b6b80a28a
unknown	gpu	TESLA V100	32.00	\N	\N	0.042222	unavailable	https://console.vast.ai/console/create/	62.80	300.00	2026-07-22 17:52:56+00	11126d65-829f-4b5e-b0a5-f5de848178b6
unknown	gpu	TESLA V100	32.00	\N	\N	0.020889	unavailable	https://console.vast.ai/console/create/	31.40	300.00	2026-07-22 17:52:56+00	60f5832c-de26-4a5e-8ff8-d86a76c7ca56
unknown	gpu	RTX 5090	31.84	\N	\N	0.294815	unavailable	https://console.vast.ai/console/create/	63.00	250.00	2026-07-22 17:52:56+00	68c09087-94c6-4ef2-b75b-735910c24e2e
unknown	gpu	RTX PRO 6000 WS	95.59	\N	\N	0.802222	available	https://console.vast.ai/console/create/	125.40	250.00	2026-07-22 17:52:56+00	554d5f10-c9ec-4e9d-9cb0-611de1f94330
unknown	gpu	H100 NVL	93.58	\N	\N	1.334815	unavailable	https://console.vast.ai/console/create/	314.70	700.00	2026-07-22 17:52:56+00	c7ff950c-0827-4195-964c-c3f4a4868328
unknown	gpu	RTX 5090	31.84	\N	\N	0.470125	available	https://console.vast.ai/console/create/	55.10	250.00	2026-07-22 17:52:56+00	349b7b2f-ba56-47d4-9fa4-979c72f303f7
unknown	gpu	RTX PRO 6000 S	95.59	\N	\N	1.002963	unavailable	https://console.vast.ai/console/create/	123.40	250.00	2026-07-22 17:52:56+00	ed3c4da2-e6c9-4a8f-b370-25e5653fd702
unknown	gpu	RTX 5070 TI	15.92	\N	\N	0.188889	unavailable	https://console.vast.ai/console/create/	125.60	250.00	2026-07-22 17:52:56+00	b649b67f-0593-45c9-800d-d6a204435ba9
unknown	gpu	RTX PRO 6000 WS	95.59	\N	\N	1.002222	unavailable	https://console.vast.ai/console/create/	167.90	250.00	2026-07-22 17:52:56+00	228fd11a-0e3e-4427-b400-33b2e2c749a5
unknown	gpu	RTX 4070S TI	15.99	\N	\N	0.080296	unavailable	https://console.vast.ai/console/create/	62.70	250.00	2026-07-22 17:52:56+00	b2b4e038-523d-4c50-ba8a-622f996c5c50
unknown	gpu	RTX 4070S TI	15.99	\N	\N	0.080296	unavailable	https://console.vast.ai/console/create/	62.60	250.00	2026-07-22 17:52:56+00	65de69a8-f896-4102-a2b3-25d8ce5af6af
unknown	gpu	RTX PRO 6000 WS	95.59	\N	\N	2.003704	unavailable	https://console.vast.ai/console/create/	335.90	250.00	2026-07-22 17:52:56+00	7126b47b-5397-476a-b74d-888de2a78933
unknown	gpu	RTX 4090	23.99	\N	\N	0.268889	unavailable	https://console.vast.ai/console/create/	62.90	450.00	2026-07-22 17:52:56+00	61fdb4e6-2e9d-469a-802f-a7e135799f0c
unknown	gpu	RTX 4090	23.99	\N	\N	0.135556	available	https://console.vast.ai/console/create/	31.40	450.00	2026-07-22 17:52:56+00	bfc6c677-a598-4350-9a18-f28feb50f44b
unknown	gpu	RTX 4090	22.49	\N	\N	0.168889	available	https://console.vast.ai/console/create/	125.90	450.00	2026-07-22 17:52:56+00	5a9f8c9c-0e0b-4726-a877-cdb656013fe1
unknown	gpu	RTX 5070 TI	15.92	\N	\N	0.122222	available	https://console.vast.ai/console/create/	62.50	250.00	2026-07-22 17:52:56+00	f2bdf724-643f-4051-8e99-fdb5bcdc8be0
unknown	gpu	RTX 5090	31.84	\N	\N	0.748889	unavailable	https://console.vast.ai/console/create/	125.60	250.00	2026-07-22 17:52:56+00	dc3fb420-028a-497c-a4d8-6b4104e2159b
unknown	gpu	RTX 5090	31.84	\N	\N	0.403704	unavailable	https://console.vast.ai/console/create/	30.50	250.00	2026-07-22 17:52:56+00	1c2634ef-7795-40a4-bce2-2c0a7833252e
unknown	gpu	RTX 5090	31.84	\N	\N	1.337037	unavailable	https://console.vast.ai/console/create/	212.40	250.00	2026-07-22 17:52:56+00	856955b8-1bb2-4f38-8d20-84bc6f249c5a
unknown	gpu	RTX 4080S	15.99	\N	\N	0.098222	unavailable	https://console.vast.ai/console/create/	62.60	320.00	2026-07-22 17:52:56+00	2fe7f4a0-8fdb-4fc7-a9b7-007d5ee22a84
unknown	gpu	RTX 3090	24.00	\N	\N	0.069630	unavailable	https://console.vast.ai/console/create/	62.70	350.00	2026-07-22 17:52:56+00	f69af36a-dc3a-42d9-a57d-bc13b7b1be5b
unknown	gpu	RTX 4080S	15.99	\N	\N	0.098222	unavailable	https://console.vast.ai/console/create/	62.60	320.00	2026-07-22 17:52:56+00	f0ced114-4a5e-4456-b624-6689e9de43f2
unknown	gpu	RTX 5070	11.94	\N	\N	0.217778	unavailable	https://console.vast.ai/console/create/	62.90	250.00	2026-07-22 17:52:56+00	c2826637-97e4-4e73-b109-6949b0eca69c
unknown	gpu	RTX 5070	11.94	\N	\N	0.111111	unavailable	https://console.vast.ai/console/create/	31.40	250.00	2026-07-22 17:52:56+00	d38ae7ea-3449-42c5-8c12-d1031c26f651
unknown	gpu	RTX PRO 4500	31.86	\N	\N	0.335556	available	https://console.vast.ai/console/create/	188.60	250.00	2026-07-22 17:52:56+00	cdd5156f-f534-4a73-aa38-e161bbca1a5f
unknown	gpu	RTX PRO 5000	47.79	\N	\N	1.280074	available	https://console.vast.ai/console/create/	125.80	250.00	2026-07-22 17:52:56+00	29aa3533-44ae-456d-af76-f6567140a910
unknown	gpu	RTX PRO 6000 WS	95.59	\N	\N	2.654370	unavailable	https://console.vast.ai/console/create/	251.80	250.00	2026-07-22 17:52:56+00	b8312227-3b6c-4c41-8a21-f84a0ddcc5a5
unknown	gpu	RTX 4090	23.99	\N	\N	0.535556	unavailable	https://console.vast.ai/console/create/	125.70	450.00	2026-07-22 17:52:56+00	01849a6b-e201-4dfb-ba2d-818dec79bfaf
unknown	gpu	RTX 5090	31.84	\N	\N	2.241481	available	https://console.vast.ai/console/create/	503.50	250.00	2026-07-22 17:52:56+00	8e2e140d-d25c-4fd1-b8ad-80e421052315
unknown	gpu	RTX 5070 TI	15.92	\N	\N	0.135556	available	https://console.vast.ai/console/create/	31.30	250.00	2026-07-22 17:52:56+00	65f6d0ae-ac4b-460f-b9b0-22054d8bb4c4
unknown	gpu	RTX 5090	31.84	\N	\N	0.938769	available	https://console.vast.ai/console/create/	110.20	250.00	2026-07-22 17:52:56+00	794a017e-347e-47d6-b612-190b8a924d84
unknown	gpu	H100 SXM	79.65	\N	\N	2.935556	unavailable	https://console.vast.ai/console/create/	431.90	700.00	2026-07-22 17:52:56+00	eba98d83-65b7-4306-8a5a-f872ca83d5b2
unknown	gpu	RTX 5070	11.94	\N	\N	0.080444	unavailable	https://console.vast.ai/console/create/	30.80	250.00	2026-07-22 17:52:56+00	e51cca3a-2622-45fa-af1d-15e2089d6bc6
unknown	gpu	RTX 5090	31.84	\N	\N	0.470370	available	https://console.vast.ai/console/create/	30.50	250.00	2026-07-22 17:52:56+00	3fc69a4f-899e-40ef-8f47-b49593eda48f
unknown	gpu	RTX 4090	47.99	\N	\N	0.935556	unavailable	https://console.vast.ai/console/create/	251.40	450.00	2026-07-22 17:52:56+00	83456c26-0e19-43d8-bf7f-12651b39f59d
unknown	gpu	RTX 5080	15.92	\N	\N	0.189630	unavailable	https://console.vast.ai/console/create/	50.30	250.00	2026-07-22 17:52:56+00	49f25d56-3ca3-4372-98c6-2527c6539017
unknown	gpu	RTX 5090	31.84	\N	\N	3.631111	unavailable	https://console.vast.ai/console/create/	566.50	250.00	2026-07-22 17:52:56+00	749a97a3-b2c6-431e-b2ab-1d06a5f16873
unknown	gpu	RTX 4090	47.99	\N	\N	0.468889	unavailable	https://console.vast.ai/console/create/	125.70	450.00	2026-07-22 17:52:56+00	52ce29cd-142f-47cb-b116-62a28eba3b84
unknown	gpu	RTX PRO 6000 S	95.59	\N	\N	2.402222	unavailable	https://console.vast.ai/console/create/	251.90	250.00	2026-07-22 17:52:56+00	c06bdd64-0787-4234-9521-e054184abed0
unknown	gpu	RTX 5080	15.92	\N	\N	0.748889	unavailable	https://console.vast.ai/console/create/	62.20	250.00	2026-07-22 17:52:56+00	22d325a8-82e1-4184-bc5b-a7d9cc3f8554
unknown	gpu	RTX 5090	31.84	\N	\N	0.561481	available	https://console.vast.ai/console/create/	125.90	250.00	2026-07-22 17:52:56+00	83c1e5b0-2c55-4981-adbb-f12c5d33acd5
unknown	gpu	RTX PRO 6000 S	95.59	\N	\N	1.736296	available	https://console.vast.ai/console/create/	125.90	250.00	2026-07-22 17:52:56+00	9a6428b7-98a5-41e3-bd95-b1108c47b2d0
unknown	gpu	RTX PRO 6000 WS	95.59	\N	\N	1.338519	unavailable	https://console.vast.ai/console/create/	94.40	250.00	2026-07-22 17:52:56+00	83f79815-1dfc-4030-bda1-2fd86b149529
unknown	gpu	RTX 5090	31.84	\N	\N	1.334370	unavailable	https://console.vast.ai/console/create/	188.80	250.00	2026-07-22 17:52:56+00	e4f6f47c-9995-4b0b-8dd5-e99f9dfa5388
unknown	gpu	RTX 5090	31.84	\N	\N	0.212889	unavailable	https://console.vast.ai/console/create/	62.60	250.00	2026-07-22 17:52:56+00	3743e50e-720b-4f05-b211-f0f17fedcd2a
unknown	gpu	RTX PRO 4500	31.86	\N	\N	0.668889	unavailable	https://console.vast.ai/console/create/	377.30	250.00	2026-07-22 17:52:56+00	4dd34944-8d50-4964-b92e-6c77d233dad7
unknown	gpu	RTX 5090	31.84	\N	\N	0.468148	available	https://console.vast.ai/console/create/	62.80	250.00	2026-07-22 17:52:56+00	570becbc-d75e-4fa9-bcd1-bd32d379eca1
unknown	gpu	H200 NVL	140.40	\N	\N	2.610222	unavailable	https://console.vast.ai/console/create/	354.20	250.00	2026-07-22 17:52:56+00	e1d82bd9-8b4d-401a-991c-2a77d9052e36
unknown	gpu	RTX 5080	15.92	\N	\N	0.188889	available	https://console.vast.ai/console/create/	30.20	250.00	2026-07-22 17:52:56+00	d5105718-f4b2-4aec-b9e7-fe479c321a3f
unknown	gpu	RTX 5070 TI	15.92	\N	\N	0.537037	unavailable	https://console.vast.ai/console/create/	125.70	250.00	2026-07-22 17:52:56+00	e83f9391-87bf-4ec0-b12e-2f90c6462249
unknown	gpu	RTX PRO 6000 S	95.59	\N	\N	3.469630	unavailable	https://console.vast.ai/console/create/	251.90	250.00	2026-07-22 17:52:56+00	a26a33d2-d402-4da4-b40c-d6580630587f
unknown	gpu	RTX 5060 TI	15.93	\N	\N	0.082222	available	https://console.vast.ai/console/create/	15.60	250.00	2026-07-22 17:52:56+00	b0009ad4-3464-4e1d-9db3-15b65bce2b31
unknown	gpu	H200 NVL	140.40	\N	\N	3.284889	available	https://console.vast.ai/console/create/	251.90	250.00	2026-07-22 17:52:56+00	bee3ebc6-efce-46d1-9387-e1dde671ff5a
unknown	gpu	RTX 3080 TI	12.00	\N	\N	0.062222	available	https://console.vast.ai/console/create/	15.60	320.00	2026-07-22 17:52:56+00	3f5fcb78-5c6d-4fbc-a41a-70be81fa49e7
unknown	gpu	RTX 4090	23.99	\N	\N	0.364444	unavailable	https://console.vast.ai/console/create/	100.80	450.00	2026-07-22 17:52:56+00	eb1d24b4-a019-47be-8bf5-a93a17b07392
unknown	gpu	RTX PRO 4500	31.86	\N	\N	0.215556	unavailable	https://console.vast.ai/console/create/	503.80	250.00	2026-07-22 17:52:56+00	00d40cc4-5b87-4f1a-9cfd-d01139e0bae5
unknown	gpu	RTX PRO 6000 WS	95.59	\N	\N	5.305037	unavailable	https://console.vast.ai/console/create/	503.70	250.00	2026-07-22 17:52:56+00	a37a6b7c-9d68-4fff-b803-151a60e414d1
unknown	gpu	RTX 4090	47.99	\N	\N	0.564444	unavailable	https://console.vast.ai/console/create/	94.40	450.00	2026-07-22 17:52:56+00	7f26c66d-7fed-4744-bb1c-8aea93af0d99
unknown	gpu	RTX 5080	15.92	\N	\N	0.324444	unavailable	https://console.vast.ai/console/create/	62.90	250.00	2026-07-22 17:52:56+00	98a06456-21c1-4ed2-aeb8-5b624aa6e10f
unknown	gpu	RTX 4090D	23.99	\N	\N	0.774815	unavailable	https://console.vast.ai/console/create/	251.80	450.00	2026-07-22 17:52:56+00	21864bd7-356c-4834-a398-d250d6257e33
unknown	gpu	RTX 5090	31.84	\N	\N	0.057778	unavailable	https://console.vast.ai/console/create/	62.80	250.00	2026-07-22 18:00:45+00	2ca5ac56-9aa9-4437-ad68-f9c3fc24ad8d
unknown	gpu	RTX 5090	31.84	\N	\N	0.111111	unavailable	https://console.vast.ai/console/create/	125.60	250.00	2026-07-22 18:00:45+00	af60e5fe-747c-43e1-b5ed-577eeb842692
unknown	gpu	TESLA V100	32.00	\N	\N	0.151556	unavailable	https://console.vast.ai/console/create/	251.10	300.00	2026-07-22 18:00:45+00	78a9457a-eb42-424a-b012-f6ef3acf54dc
unknown	gpu	TESLA V100	32.00	\N	\N	0.039556	unavailable	https://console.vast.ai/console/create/	62.80	300.00	2026-07-22 18:00:45+00	3cce5761-d5e3-4f4b-91d5-4cf8b5ce41ee
unknown	gpu	TESLA V100	32.00	\N	\N	0.087556	unavailable	https://console.vast.ai/console/create/	125.50	300.00	2026-07-22 18:00:45+00	6dd1d1c7-d21a-4e1d-9eb9-08a99eefeddd
unknown	gpu	TESLA V100	32.00	\N	\N	0.020889	unavailable	https://console.vast.ai/console/create/	31.40	300.00	2026-07-22 18:00:45+00	46396d07-9056-4791-8a1e-6bc0b9cc23c4
unknown	gpu	RTX PRO 6000 WS	95.59	\N	\N	0.802222	available	https://console.vast.ai/console/create/	125.40	250.00	2026-07-22 18:00:45+00	a7831380-f290-45de-b287-549cd621d6e1
unknown	gpu	RTX 5090	31.84	\N	\N	0.911111	available	https://console.vast.ai/console/create/	141.60	250.00	2026-07-22 18:00:45+00	77ab954a-e221-44b6-a351-953291f02f75
unknown	gpu	RTX 5090	31.84	\N	\N	0.298222	available	https://console.vast.ai/console/create/	62.50	250.00	2026-07-22 18:00:45+00	0ec3b309-5207-477b-a656-267b0b7d5e04
unknown	gpu	RTX PRO 6000 WS	95.59	\N	\N	0.934815	unavailable	https://console.vast.ai/console/create/	125.60	250.00	2026-07-22 18:00:45+00	e54d6e6f-e9d3-41d0-baba-5dcbf32d0f0d
unknown	gpu	RTX 5090	31.84	\N	\N	0.375556	unavailable	https://console.vast.ai/console/create/	62.80	250.00	2026-07-22 18:00:45+00	62d48f6d-6d40-42d2-bd4e-c4328c51a85f
unknown	gpu	RTX 4090	23.99	\N	\N	0.168889	available	https://console.vast.ai/console/create/	125.90	450.00	2026-07-22 18:00:45+00	5714017d-0fc6-42f5-9600-b40e98682e59
unknown	gpu	RTX 5090	31.84	\N	\N	1.017037	unavailable	https://console.vast.ai/console/create/	220.20	250.00	2026-07-22 18:00:45+00	7bf23e6d-e40b-4520-b99b-0d43ffa60738
unknown	gpu	RTX PRO 6000 WS	95.59	\N	\N	2.207556	unavailable	https://console.vast.ai/console/create/	377.20	250.00	2026-07-22 18:00:45+00	cdbba0e2-fbc6-468e-a8a0-0cb3a51ba32d
unknown	gpu	RTX PRO 6000 WS	95.59	\N	\N	1.682222	unavailable	https://console.vast.ai/console/create/	345.90	250.00	2026-07-22 18:00:45+00	48713165-d98c-4488-98a9-1d717122006f
unknown	gpu	RTX 5070 TI	15.92	\N	\N	0.122222	available	https://console.vast.ai/console/create/	62.50	250.00	2026-07-22 18:00:45+00	0fb2adcd-e25d-4442-9a7a-7bb7da42d40f
unknown	gpu	RTX 4090	23.99	\N	\N	0.135556	available	https://console.vast.ai/console/create/	31.40	450.00	2026-07-22 18:00:45+00	dceb97e8-ebd1-4a9c-81e3-c0facb11cf81
unknown	gpu	H100 SXM	79.65	\N	\N	1.468889	unavailable	https://console.vast.ai/console/create/	215.90	700.00	2026-07-22 18:00:45+00	6bdcc96a-36f2-4cfc-bbe0-fc77490094cd
unknown	gpu	RTX 4080S	15.99	\N	\N	0.096296	unavailable	https://console.vast.ai/console/create/	62.60	320.00	2026-07-22 18:00:45+00	796b4625-07c5-4fba-b844-8da97b569b56
unknown	gpu	RTX 4090	23.99	\N	\N	0.268889	available	https://console.vast.ai/console/create/	62.90	450.00	2026-07-22 18:00:45+00	8ab98c89-dc8d-46d3-84e5-fae58e56358b
unknown	gpu	RTX 5090	31.84	\N	\N	0.414222	available	https://console.vast.ai/console/create/	31.40	250.00	2026-07-22 18:00:45+00	1952ccb2-45f5-4615-bd60-1acf9c0c2055
unknown	gpu	RTX 5090	31.84	\N	\N	0.403704	unavailable	https://console.vast.ai/console/create/	30.50	250.00	2026-07-22 18:00:45+00	22419253-4732-438b-8960-e0c0ff642dff
unknown	gpu	RTX 5070	11.94	\N	\N	0.431111	unavailable	https://console.vast.ai/console/create/	125.80	250.00	2026-07-22 18:00:45+00	705e89f9-c76f-4429-9a7a-583aefc867d8
unknown	gpu	RTX 5090	31.84	\N	\N	0.826222	available	https://console.vast.ai/console/create/	62.80	250.00	2026-07-22 18:00:45+00	267398c5-57a5-472f-86db-d7b7632fbe5f
unknown	gpu	RTX 4080S	15.99	\N	\N	0.098222	available	https://console.vast.ai/console/create/	62.60	320.00	2026-07-22 18:00:45+00	1a7f8b4a-5421-46f6-ab4b-c41d200437f3
unknown	gpu	RTX PRO 4500	31.86	\N	\N	0.322222	unavailable	https://console.vast.ai/console/create/	125.30	250.00	2026-07-22 18:00:45+00	cf7d2f4b-4321-402a-9c48-adc75cc2f64a
unknown	gpu	RTX 3090	24.00	\N	\N	0.069630	unavailable	https://console.vast.ai/console/create/	62.70	350.00	2026-07-22 18:00:45+00	a6903d1a-299c-4500-aa32-c6693eec817e
unknown	gpu	RTX 4090	47.99	\N	\N	0.590370	unavailable	https://console.vast.ai/console/create/	125.90	450.00	2026-07-22 18:00:45+00	e9b3f6c1-4da7-46af-8a40-c1e99024faa6
unknown	gpu	RTX 4090	47.99	\N	\N	0.297037	unavailable	https://console.vast.ai/console/create/	62.90	450.00	2026-07-22 18:00:45+00	94aa695a-6279-4684-9eac-4dba8de6886b
unknown	gpu	RTX 5070	11.94	\N	\N	0.111111	unavailable	https://console.vast.ai/console/create/	31.40	250.00	2026-07-22 18:00:45+00	de15300b-2384-4146-bc4a-31a81705077d
unknown	gpu	RTX 5070 TI	15.92	\N	\N	0.242222	available	https://console.vast.ai/console/create/	62.80	250.00	2026-07-22 18:00:45+00	67ad15b8-c9a5-4c86-823d-e2f669b86bc6
unknown	gpu	RTX 5070 TI	15.92	\N	\N	0.263556	unavailable	https://console.vast.ai/console/create/	60.40	250.00	2026-07-22 18:00:45+00	5508820a-d13c-48b6-af19-eee17b84ab20
unknown	gpu	RTX PRO 6000 S	95.59	\N	\N	1.468889	unavailable	https://console.vast.ai/console/create/	124.80	250.00	2026-07-22 18:00:45+00	d6588d06-ae89-4802-8b21-e47746fc3bda
unknown	gpu	RTX 5070 TI	15.92	\N	\N	0.135556	available	https://console.vast.ai/console/create/	31.30	250.00	2026-07-22 18:00:45+00	5d3bde91-0242-4d81-bc82-262d683edf0e
unknown	gpu	RTX PRO 6000 S	95.59	\N	\N	2.669630	unavailable	https://console.vast.ai/console/create/	377.80	250.00	2026-07-22 18:00:45+00	c9c3f4e0-daa6-4d61-8afd-c18b077c7772
unknown	gpu	RTX 5070	11.94	\N	\N	0.244444	unavailable	https://console.vast.ai/console/create/	83.50	250.00	2026-07-22 18:00:45+00	e5a4398e-e4d3-4c34-8e2d-93abdf8020bd
unknown	gpu	H100 SXM	79.65	\N	\N	2.935556	unavailable	https://console.vast.ai/console/create/	431.90	700.00	2026-07-22 18:00:45+00	8afcc51a-ec1e-4b7f-9753-c8dc8a951a6b
unknown	gpu	RTX 4090	23.99	\N	\N	0.535556	unavailable	https://console.vast.ai/console/create/	125.70	450.00	2026-07-22 18:00:45+00	5c66b72f-77ba-4a03-a6eb-abea119fcf5a
unknown	gpu	RTX 5090	31.84	\N	\N	2.241481	available	https://console.vast.ai/console/create/	503.50	250.00	2026-07-22 18:00:45+00	f8e773c8-ef8c-459c-9f9d-389c87ede892
unknown	gpu	RTX 5090	31.84	\N	\N	0.470370	available	https://console.vast.ai/console/create/	30.50	250.00	2026-07-22 18:00:45+00	a3bb3621-f83a-4a44-8143-964c14c7f775
unknown	gpu	RTX PRO 6000 WS	95.59	\N	\N	1.329037	unavailable	https://console.vast.ai/console/create/	125.90	250.00	2026-07-22 18:00:45+00	b9ac1802-a03a-42f3-a5cd-e46cf5f71130
unknown	gpu	RTX PRO 5000	47.79	\N	\N	0.538519	unavailable	https://console.vast.ai/console/create/	62.90	250.00	2026-07-22 18:00:45+00	26989586-d781-458d-80c2-62d235213b46
unknown	gpu	RTX 5090	31.84	\N	\N	1.334370	unavailable	https://console.vast.ai/console/create/	188.80	250.00	2026-07-22 18:00:45+00	f9062aaf-2e7d-4445-8d99-12f051c5385f
unknown	gpu	RTX 4090	47.99	\N	\N	0.935556	unavailable	https://console.vast.ai/console/create/	251.40	450.00	2026-07-22 18:00:45+00	15cc711a-6304-4562-bf2a-54e53a04bb7a
unknown	gpu	RTX 5090	31.84	\N	\N	0.470370	available	https://console.vast.ai/console/create/	30.50	250.00	2026-07-22 18:00:45+00	4bfc2e24-ebe4-48fb-b486-03b2e74e1086
unknown	gpu	RTX PRO 5000	47.79	\N	\N	2.560074	available	https://console.vast.ai/console/create/	251.70	250.00	2026-07-22 18:00:45+00	800df428-5583-42fb-97f7-c7e9e24ffb08
unknown	gpu	RTX 5090	31.84	\N	\N	3.631111	unavailable	https://console.vast.ai/console/create/	566.50	250.00	2026-07-22 18:00:45+00	5966f9f1-b1da-4dae-84a1-94755c0d0cb9
unknown	gpu	RTX 4090	23.99	\N	\N	0.455556	unavailable	https://console.vast.ai/console/create/	62.80	450.00	2026-07-22 18:00:45+00	49f00f39-f206-494a-9922-e9ec46762b3e
unknown	gpu	RTX PRO 5000	47.79	\N	\N	1.071852	unavailable	https://console.vast.ai/console/create/	125.80	250.00	2026-07-22 18:00:45+00	4fe348c1-e452-406e-aee4-efe21ff7d72c
unknown	gpu	RTX 5080	15.92	\N	\N	0.324444	unavailable	https://console.vast.ai/console/create/	62.90	250.00	2026-07-22 18:00:45+00	a574052b-5a9f-4457-8c70-c1c4df9896cb
unknown	gpu	RTX PRO 6000 S	95.59	\N	\N	1.736296	unavailable	https://console.vast.ai/console/create/	125.90	250.00	2026-07-22 18:00:45+00	4c3f2785-1df6-4d32-bf7d-554a528a3848
unknown	gpu	RTX 5080	15.92	\N	\N	0.177778	unavailable	https://console.vast.ai/console/create/	31.40	250.00	2026-07-22 18:00:45+00	71f1745f-361f-4f18-9c05-443c68102eaa
unknown	gpu	RTX 5080	15.92	\N	\N	0.228889	unavailable	https://console.vast.ai/console/create/	30.90	250.00	2026-07-22 18:00:45+00	46cc9804-9b3c-4de2-a844-d7e942d5b83f
unknown	gpu	RTX 5070	11.94	\N	\N	0.857778	unavailable	https://console.vast.ai/console/create/	251.50	250.00	2026-07-22 18:00:45+00	ca151fb6-b385-40a0-9864-c55800bc635f
unknown	gpu	RTX 5070	11.94	\N	\N	0.080444	unavailable	https://console.vast.ai/console/create/	30.80	250.00	2026-07-22 18:00:45+00	066df026-1064-4d66-a4bd-5661982836af
unknown	gpu	H200 NVL	140.40	\N	\N	3.204889	unavailable	https://console.vast.ai/console/create/	251.90	250.00	2026-07-22 18:00:45+00	643b0d7a-f64d-421a-b77c-78802a9c7849
unknown	gpu	RTX 5090	31.84	\N	\N	0.212889	unavailable	https://console.vast.ai/console/create/	62.60	250.00	2026-07-22 18:00:45+00	d603ae92-cc89-4934-aa4b-b408a00c4f08
unknown	gpu	RTX PRO 6000 S	95.59	\N	\N	3.469630	unavailable	https://console.vast.ai/console/create/	251.90	250.00	2026-07-22 18:00:45+00	131e9646-b0b2-4888-9db7-e2722860a446
unknown	gpu	RTX 5080	15.92	\N	\N	0.122222	unavailable	https://console.vast.ai/console/create/	55.00	250.00	2026-07-22 18:00:45+00	4f46ca8b-4242-41ec-9417-8412494f4460
unknown	gpu	H200 NVL	140.40	\N	\N	25.381778	unavailable	https://console.vast.ai/console/create/	2015.50	250.00	2026-07-22 18:00:45+00	2cdfeb94-edd8-40d8-80bd-9f91598bbc96
unknown	gpu	RTX 6000ADA	47.99	\N	\N	0.783556	available	https://console.vast.ai/console/create/	167.90	250.00	2026-07-22 18:00:45+00	87dafc7b-f987-4bcc-8ec8-8a108ea0e329
unknown	gpu	H200 NVL	140.40	\N	\N	12.693778	unavailable	https://console.vast.ai/console/create/	1007.70	250.00	2026-07-22 18:00:45+00	b751da68-e2c5-4053-b869-9672116b6bb6
unknown	gpu	RTX 4090D	23.99	\N	\N	0.388148	unavailable	https://console.vast.ai/console/create/	125.90	450.00	2026-07-22 18:00:45+00	4605b288-1d05-4588-81d3-8158d9023bc7
unknown	gpu	RTX PRO 6000 WS	95.59	\N	\N	5.305037	unavailable	https://console.vast.ai/console/create/	503.70	250.00	2026-07-22 18:00:45+00	fd8ea848-0a5b-4b31-9162-c91313a738dc
unknown	gpu	RTX 5090	31.84	\N	\N	0.057778	available	https://console.vast.ai/console/create/	62.80	250.00	2026-07-22 18:01:10+00	ae00c848-3d93-48ca-a42a-f22c6aee7394
unknown	gpu	RTX 5090	31.84	\N	\N	0.111111	unavailable	https://console.vast.ai/console/create/	125.60	250.00	2026-07-22 18:01:10+00	1d390dd0-d145-4644-adb7-97092053f5ab
unknown	gpu	TESLA V100	32.00	\N	\N	0.151556	unavailable	https://console.vast.ai/console/create/	251.10	300.00	2026-07-22 18:01:10+00	29dbc368-df22-4eb1-91d4-8ced6fdf435e
unknown	gpu	TESLA V100	32.00	\N	\N	0.076889	unavailable	https://console.vast.ai/console/create/	94.00	300.00	2026-07-22 18:01:10+00	343a61f5-4895-437b-9389-72800ebd2e82
unknown	gpu	TESLA V100	32.00	\N	\N	0.039556	unavailable	https://console.vast.ai/console/create/	62.80	300.00	2026-07-22 18:01:10+00	fa5e0a3e-309a-4678-a73c-986e18a4895e
unknown	gpu	TESLA V100	32.00	\N	\N	0.024889	unavailable	https://console.vast.ai/console/create/	31.40	300.00	2026-07-22 18:01:10+00	be2eaf2b-7360-4f24-9d88-5f934ce0b58e
unknown	gpu	RTX PRO 6000 S	95.59	\N	\N	0.774756	unavailable	https://console.vast.ai/console/create/	124.80	250.00	2026-07-22 18:01:10+00	fffe2c2c-b6c6-4e24-848b-2b88bd91c895
unknown	gpu	RTX 5070 TI	15.92	\N	\N	0.095556	unavailable	https://console.vast.ai/console/create/	62.80	250.00	2026-07-22 18:01:10+00	d8f8d2c7-5f66-45fb-8213-805db476a6eb
unknown	gpu	RTX 5090	31.84	\N	\N	0.457778	unavailable	https://console.vast.ai/console/create/	70.80	250.00	2026-07-22 18:01:10+00	2d57610a-3191-48d6-b5a5-e1356340d2b9
unknown	gpu	RTX 5090	31.84	\N	\N	0.911111	unavailable	https://console.vast.ai/console/create/	141.60	250.00	2026-07-22 18:01:10+00	bfde93f6-20dc-46ee-8566-51140598222b
unknown	gpu	RTX 5090	31.84	\N	\N	0.375556	unavailable	https://console.vast.ai/console/create/	62.80	250.00	2026-07-22 18:01:10+00	05fc0a3c-48d6-4ae8-bdb1-0e065e35a661
unknown	gpu	RTX PRO 6000 WS	95.59	\N	\N	1.002963	unavailable	https://console.vast.ai/console/create/	167.90	250.00	2026-07-22 18:01:10+00	9498edad-2217-4557-8163-0d22c7a11699
unknown	gpu	RTX 5090	31.84	\N	\N	0.938519	unavailable	https://console.vast.ai/console/create/	188.90	250.00	2026-07-22 18:01:10+00	6b23df23-d8c0-4658-8ca6-3bfdc6866163
unknown	gpu	RTX PRO 6000 WS	95.59	\N	\N	1.841630	unavailable	https://console.vast.ai/console/create/	188.30	250.00	2026-07-22 18:01:10+00	11720c80-7902-4395-93a6-145191f4683b
unknown	gpu	RTX PRO 6000 WS	95.59	\N	\N	2.335556	unavailable	https://console.vast.ai/console/create/	251.40	250.00	2026-07-22 18:01:10+00	8ebf0aff-9c1a-46a1-a122-20c673eac90b
unknown	gpu	RTX PRO 6000 WS	95.59	\N	\N	0.935556	available	https://console.vast.ai/console/create/	125.60	250.00	2026-07-22 18:01:10+00	435a71af-03c9-45f8-9876-e83af03970f0
unknown	gpu	RTX 5070 TI	15.92	\N	\N	0.188889	unavailable	https://console.vast.ai/console/create/	125.60	250.00	2026-07-22 18:01:10+00	e9dee222-6164-459f-9173-b05b3c00c18f
unknown	gpu	RTX 5090	31.84	\N	\N	0.414222	available	https://console.vast.ai/console/create/	31.40	250.00	2026-07-22 18:01:10+00	8715ca91-7245-4a8c-acbc-b4c0b4e7069e
unknown	gpu	RTX 4090	23.99	\N	\N	0.135556	unavailable	https://console.vast.ai/console/create/	31.40	450.00	2026-07-22 18:01:10+00	bd59832f-e4a1-4b56-80cd-3616a1d9023b
unknown	gpu	RTX 4090	23.99	\N	\N	0.268889	unavailable	https://console.vast.ai/console/create/	62.90	450.00	2026-07-22 18:01:10+00	09d43210-e767-4f92-8700-3e6c7e604c4d
unknown	gpu	RTX 4090	23.99	\N	\N	0.182222	unavailable	https://console.vast.ai/console/create/	62.80	450.00	2026-07-22 18:01:10+00	783a4523-7870-4d91-a380-22373a906aec
unknown	gpu	RTX 4090	47.99	\N	\N	0.297037	unavailable	https://console.vast.ai/console/create/	62.90	450.00	2026-07-22 18:01:10+00	74858b30-374a-41ec-938e-18b5f1eed798
unknown	gpu	RTX 5070 TI	15.92	\N	\N	0.122222	available	https://console.vast.ai/console/create/	62.50	250.00	2026-07-22 18:01:10+00	5f2adf03-0b11-449b-8daa-492d8a542d62
unknown	gpu	RTX 5070	11.94	\N	\N	0.217778	unavailable	https://console.vast.ai/console/create/	62.90	250.00	2026-07-22 18:01:10+00	c9851977-0ba4-4125-9634-9f5b67899dc3
unknown	gpu	RTX 5090	31.84	\N	\N	0.403704	unavailable	https://console.vast.ai/console/create/	30.50	250.00	2026-07-22 18:01:10+00	bc36c5ed-35e3-4c80-a08f-a2186ca5a592
unknown	gpu	RTX 4080S	15.99	\N	\N	0.098222	unavailable	https://console.vast.ai/console/create/	62.60	320.00	2026-07-22 18:01:10+00	f916fb9a-fb6d-422f-808c-d0b4fc93c20d
unknown	gpu	RTX PRO 6000 S	95.59	\N	\N	1.268889	unavailable	https://console.vast.ai/console/create/	125.90	250.00	2026-07-22 18:01:10+00	f3c0c423-8a6e-424a-994f-586262ce6284
unknown	gpu	H100 SXM	79.65	\N	\N	2.935556	unavailable	https://console.vast.ai/console/create/	431.90	700.00	2026-07-22 18:01:10+00	e9259e6e-b7eb-410e-8d4b-eb04dd67580f
unknown	gpu	RTX 5070	11.94	\N	\N	0.111111	unavailable	https://console.vast.ai/console/create/	31.40	250.00	2026-07-22 18:01:10+00	2ea70bf3-e550-412e-82d2-2609717df85a
unknown	gpu	RTX PRO 6000 WS	95.59	\N	\N	2.654370	unavailable	https://console.vast.ai/console/create/	251.80	250.00	2026-07-22 18:01:10+00	0505a05d-8462-496e-9965-78b027dedeb6
unknown	gpu	RTX 4090	47.99	\N	\N	0.937037	unavailable	https://console.vast.ai/console/create/	188.90	450.00	2026-07-22 18:01:10+00	e5ffb95b-b0fd-46e4-a421-1f8e7462ada7
unknown	gpu	RTX 4090	23.99	\N	\N	0.535556	unavailable	https://console.vast.ai/console/create/	125.70	450.00	2026-07-22 18:01:10+00	7b58a883-4f4b-402b-88ad-fb2474eeb7cd
unknown	gpu	L4	22.49	\N	\N	0.032593	unavailable	https://console.vast.ai/console/create/	24.80	250.00	2026-07-22 18:01:10+00	3d6f169f-498c-477a-8d1e-5de88c41d9bd
unknown	gpu	H100 NVL	93.58	\N	\N	1.842222	unavailable	https://console.vast.ai/console/create/	314.70	700.00	2026-07-22 18:01:10+00	9bbfad85-8866-4a1a-a275-75561ca88785
unknown	gpu	RTX 4090	47.99	\N	\N	0.935556	unavailable	https://console.vast.ai/console/create/	251.40	450.00	2026-07-22 18:01:10+00	79fb529a-36ea-457f-91fa-639b38ccc6a5
unknown	gpu	RTX 5080	15.92	\N	\N	0.164444	unavailable	https://console.vast.ai/console/create/	31.40	250.00	2026-07-22 18:01:10+00	fecc282b-e121-48b9-a30b-236c7f99f641
unknown	gpu	RTX 4090	23.99	\N	\N	0.455556	unavailable	https://console.vast.ai/console/create/	62.80	450.00	2026-07-22 18:01:10+00	c8af7476-d9aa-4fb3-ad64-340e244fac2d
unknown	gpu	RTX 5090	31.84	\N	\N	2.241481	available	https://console.vast.ai/console/create/	503.50	250.00	2026-07-22 18:01:10+00	c6a652c5-5d66-4d53-9792-a601030e51b5
unknown	gpu	RTX PRO 6000 WS	95.59	\N	\N	1.329037	unavailable	https://console.vast.ai/console/create/	125.90	250.00	2026-07-22 18:01:10+00	c157534e-cf0f-40fc-939b-7e954639f324
unknown	gpu	RTX PRO 5000	47.79	\N	\N	1.280074	available	https://console.vast.ai/console/create/	125.80	250.00	2026-07-22 18:01:10+00	f52da55d-e165-42fd-b91e-0c35bcd0bdb6
unknown	gpu	RTX 5070	11.94	\N	\N	0.857778	unavailable	https://console.vast.ai/console/create/	251.50	250.00	2026-07-22 18:01:10+00	aeb6163c-5989-470d-87a3-ad0775bdd1f5
unknown	gpu	RTX 5090	31.84	\N	\N	0.470370	unavailable	https://console.vast.ai/console/create/	30.50	250.00	2026-07-22 18:01:10+00	747e256f-2cf2-460e-99b7-6a0ed241ff55
unknown	gpu	RTX 5090	31.84	\N	\N	0.212889	unavailable	https://console.vast.ai/console/create/	62.60	250.00	2026-07-22 18:01:10+00	5011c12f-736a-4195-a0dc-7587b35dfcdb
unknown	gpu	RTX 5060 TI	15.93	\N	\N	0.054074	unavailable	https://console.vast.ai/console/create/	31.30	250.00	2026-07-22 18:01:10+00	d0d87258-8605-476d-95dd-f7685f1b523f
unknown	gpu	RTX 5080	15.92	\N	\N	0.748889	unavailable	https://console.vast.ai/console/create/	62.20	250.00	2026-07-22 18:01:10+00	d186c197-b437-4873-b556-db4a2daa909c
unknown	gpu	RTX 4080S	15.99	\N	\N	0.098222	unavailable	https://console.vast.ai/console/create/	62.60	320.00	2026-07-22 18:01:10+00	b88ee406-55cb-4b37-a776-034d39d6668f
unknown	gpu	RTX 5090	31.84	\N	\N	1.307704	unavailable	https://console.vast.ai/console/create/	188.80	250.00	2026-07-22 18:01:10+00	2df270a5-f2e9-44d7-8613-3f585c585492
unknown	gpu	RTX 4090	23.99	\N	\N	0.362222	unavailable	https://console.vast.ai/console/create/	125.60	450.00	2026-07-22 18:01:10+00	dcc6ba26-3844-4f9c-acb3-804bdcd2cb7f
unknown	gpu	RTX 4090	23.99	\N	\N	0.294815	unavailable	https://console.vast.ai/console/create/	94.10	450.00	2026-07-22 18:01:10+00	c498d4fb-5d1c-43f4-87a9-d70ed5ff7ed2
unknown	gpu	RTX 5080	15.92	\N	\N	0.351111	unavailable	https://console.vast.ai/console/create/	62.90	250.00	2026-07-22 18:01:10+00	47b34714-cd52-451d-b332-18c703904ca0
unknown	gpu	RTX PRO 6000 S	95.59	\N	\N	2.535556	available	https://console.vast.ai/console/create/	188.90	250.00	2026-07-22 18:01:10+00	9eab9c4a-f38d-4c36-9041-1a505e629e55
unknown	gpu	RTX 5060 TI	15.93	\N	\N	0.077037	unavailable	https://console.vast.ai/console/create/	31.40	250.00	2026-07-22 18:01:10+00	a6e6c8bd-83be-4598-b77b-9bac8a5f87f3
unknown	gpu	RTX 5070 TI	15.92	\N	\N	0.537037	unavailable	https://console.vast.ai/console/create/	125.60	250.00	2026-07-22 18:01:10+00	18ac43a3-8517-4aab-8524-0b8f6292a5c7
unknown	gpu	RTX 5090	31.84	\N	\N	0.561481	available	https://console.vast.ai/console/create/	125.90	250.00	2026-07-22 18:01:10+00	d1141fc5-9a07-4592-9144-a09a52b504b8
unknown	gpu	RTX PRO 6000 S	95.59	\N	\N	3.469630	available	https://console.vast.ai/console/create/	251.70	250.00	2026-07-22 18:01:10+00	5e8ab878-64f3-4579-941c-ebf28e7529c9
unknown	gpu	RTX PRO 6000 S	95.59	\N	\N	1.736296	unavailable	https://console.vast.ai/console/create/	125.90	250.00	2026-07-22 18:01:10+00	813e2d53-a99d-4304-8697-2a7184823818
unknown	gpu	RTX 5070 TI	15.92	\N	\N	0.268889	available	https://console.vast.ai/console/create/	62.60	250.00	2026-07-22 18:01:10+00	362033d0-f43e-4d2b-be70-c41c1668ab89
unknown	gpu	H200 NVL	140.40	\N	\N	3.177778	unavailable	https://console.vast.ai/console/create/	251.90	250.00	2026-07-22 18:01:10+00	0e922133-384b-4c7a-bdd2-d8cd7d0c56b6
unknown	gpu	H200 NVL	140.40	\N	\N	12.693778	unavailable	https://console.vast.ai/console/create/	1007.70	250.00	2026-07-22 18:01:10+00	864b528e-3193-4c64-bea3-07ac86e73dd0
unknown	gpu	RTX 5090	31.84	\N	\N	3.631111	unavailable	https://console.vast.ai/console/create/	566.50	250.00	2026-07-22 18:01:10+00	eee2f074-e1bd-4898-bf8d-6c1142296c60
unknown	gpu	H200 NVL	140.40	\N	\N	25.381778	unavailable	https://console.vast.ai/console/create/	2015.50	250.00	2026-07-22 18:01:10+00	9d2d1523-2c57-4410-acbb-a7fe0403ce13
unknown	gpu	RTX 5090	31.84	\N	\N	0.403704	available	https://console.vast.ai/console/create/	30.50	250.00	2026-07-22 18:01:10+00	bccbb5ee-afea-462e-998e-e295cf98420b
unknown	gpu	RTX 4090D	47.99	\N	\N	0.402963	unavailable	https://console.vast.ai/console/create/	94.20	450.00	2026-07-22 18:01:10+00	f81d70de-92f0-4dc4-89ab-0f2a7a738b7b
unknown	gpu	H200 NVL	140.40	\N	\N	6.349778	unavailable	https://console.vast.ai/console/create/	503.90	250.00	2026-07-22 18:01:10+00	7be39860-3143-4c7a-a2df-8170e9370158
unknown	gpu	RTX 5090	31.84	\N	\N	0.057778	unavailable	https://console.vast.ai/console/create/	62.80	250.00	2026-07-22 19:09:21+00	9efb2962-c217-4b3d-9c84-55461ab0026a
unknown	gpu	RTX 5090	31.84	\N	\N	0.111111	unavailable	https://console.vast.ai/console/create/	125.60	250.00	2026-07-22 19:09:21+00	0fe89920-a6d2-4cf1-9151-9a8c95f3ea12
unknown	gpu	TESLA V100	32.00	\N	\N	0.151556	unavailable	https://console.vast.ai/console/create/	188.10	300.00	2026-07-22 19:09:21+00	ffa70135-dd14-4e3a-9225-43c546dffd50
unknown	gpu	TESLA V100	32.00	\N	\N	0.042222	unavailable	https://console.vast.ai/console/create/	62.80	300.00	2026-07-22 19:09:21+00	139e6e10-ebc2-4f8b-a9f9-75c5519d309d
unknown	gpu	TESLA V100	32.00	\N	\N	0.087556	unavailable	https://console.vast.ai/console/create/	125.50	300.00	2026-07-22 19:09:21+00	f1997b86-734d-4c04-b2dc-2215c712aac6
unknown	gpu	TESLA V100	32.00	\N	\N	0.020889	unavailable	https://console.vast.ai/console/create/	31.40	300.00	2026-07-22 19:09:21+00	b22e7ce6-e315-4491-b003-a304c6886f1a
unknown	gpu	RTX 5070 TI	15.92	\N	\N	0.095556	unavailable	https://console.vast.ai/console/create/	62.80	250.00	2026-07-22 19:09:21+00	549a0a5f-b673-4357-8631-b3434a259731
unknown	gpu	RTX 5090	31.84	\N	\N	0.375556	unavailable	https://console.vast.ai/console/create/	62.80	250.00	2026-07-22 19:09:21+00	9fdadbf2-dcb3-47e8-9b76-0678cffd7d96
unknown	gpu	RTX 5090	31.84	\N	\N	0.457778	unavailable	https://console.vast.ai/console/create/	70.80	250.00	2026-07-22 19:09:21+00	2f92acde-9b90-4a29-8929-01e0a8a5fd9e
unknown	gpu	RTX PRO 6000 WS	95.59	\N	\N	1.002222	unavailable	https://console.vast.ai/console/create/	167.90	250.00	2026-07-22 19:09:21+00	cba39d17-1010-46aa-889a-3fe94cd51db9
unknown	gpu	RTX PRO 6000 WS	95.59	\N	\N	0.736296	unavailable	https://console.vast.ai/console/create/	124.70	250.00	2026-07-22 19:09:21+00	133e0e5e-8fa0-49ae-b6e5-5993b444c3fe
unknown	gpu	RTX 5090	31.84	\N	\N	1.121481	available	https://console.vast.ai/console/create/	251.80	250.00	2026-07-22 19:09:21+00	80cd792d-3cdf-49ac-be3a-034395689e34
unknown	gpu	RTX 5090	31.84	\N	\N	1.017037	unavailable	https://console.vast.ai/console/create/	220.20	250.00	2026-07-22 19:09:21+00	130f101d-3bdd-479d-8469-13d53d11ad42
unknown	gpu	RTX 5090	31.84	\N	\N	0.281481	available	https://console.vast.ai/console/create/	63.00	250.00	2026-07-22 19:09:21+00	06715a81-0640-44be-a3cd-66e34b9ce719
unknown	gpu	RTX 4090	22.49	\N	\N	0.168889	available	https://console.vast.ai/console/create/	125.90	450.00	2026-07-22 19:09:21+00	0d09d8b1-0242-47c0-b769-57529f07b13d
unknown	gpu	RTX PRO 6000 S	95.59	\N	\N	1.202222	unavailable	https://console.vast.ai/console/create/	125.90	250.00	2026-07-22 19:09:21+00	38e2c8e8-b94c-4366-b718-7bc498ee7070
unknown	gpu	RTX 4070S TI	15.99	\N	\N	0.082222	unavailable	https://console.vast.ai/console/create/	62.60	250.00	2026-07-22 19:09:21+00	31335695-03c6-4ebd-8332-a729e9258524
unknown	gpu	RTX 5090	31.84	\N	\N	1.284444	unavailable	https://console.vast.ai/console/create/	251.40	250.00	2026-07-22 19:09:21+00	d0394089-2ba6-4137-bc34-6b9ec4a6c905
unknown	gpu	RTX 4090	23.99	\N	\N	0.268889	unavailable	https://console.vast.ai/console/create/	62.90	450.00	2026-07-22 19:09:21+00	36dee2c5-ef4f-46c9-9a61-34262ed20305
unknown	gpu	RTX 4090	23.99	\N	\N	0.135556	available	https://console.vast.ai/console/create/	31.40	450.00	2026-07-22 19:09:21+00	2bc92f7a-938b-411f-a2d1-17f5193ba416
unknown	gpu	RTX 4080S	15.99	\N	\N	0.098222	unavailable	https://console.vast.ai/console/create/	62.60	320.00	2026-07-22 19:09:21+00	dc861e20-7097-4489-8566-a1b5a4cdba79
unknown	gpu	H100 SXM	79.65	\N	\N	1.468889	unavailable	https://console.vast.ai/console/create/	215.90	700.00	2026-07-22 19:09:21+00	347db025-1e1a-449e-b7c7-838b688ff0f8
unknown	gpu	RTX 5090	31.84	\N	\N	0.403704	unavailable	https://console.vast.ai/console/create/	30.50	250.00	2026-07-22 19:09:21+00	38c3a7e3-b914-48b6-92a2-042286bdae08
unknown	gpu	RTX 5070 TI	15.92	\N	\N	0.101481	unavailable	https://console.vast.ai/console/create/	30.20	250.00	2026-07-22 19:09:21+00	9b4110b4-317a-4612-afbd-0e4a93f79c1d
unknown	gpu	RTX PRO 6000 WS	95.59	\N	\N	2.654370	unavailable	https://console.vast.ai/console/create/	251.80	250.00	2026-07-22 19:09:21+00	406da197-7120-42ab-b544-fd2d094ffb98
unknown	gpu	RTX 5090	31.84	\N	\N	0.826222	available	https://console.vast.ai/console/create/	62.80	250.00	2026-07-22 19:09:21+00	b6ea2836-5cc3-4fcf-9e3f-5ff04e2a042e
unknown	gpu	RTX 4090	47.99	\N	\N	0.297037	unavailable	https://console.vast.ai/console/create/	62.90	450.00	2026-07-22 19:09:21+00	d14bfeaa-ffb8-4ceb-aaa0-ebbd56f8044d
unknown	gpu	RTX 4090	22.49	\N	\N	0.335556	available	https://console.vast.ai/console/create/	251.70	450.00	2026-07-22 19:09:21+00	b408363a-275a-4b7c-93a3-2a5322f378d0
unknown	gpu	RTX 4080S	15.99	\N	\N	0.098222	available	https://console.vast.ai/console/create/	62.60	320.00	2026-07-22 19:09:21+00	d7584eb6-0cbf-45c0-9272-9fbe2d9affbd
unknown	gpu	RTX 5080	15.92	\N	\N	0.143452	unavailable	https://console.vast.ai/console/create/	92.20	250.00	2026-07-22 19:09:21+00	d36ee789-c9e5-408c-987e-13e665a3a746
unknown	gpu	RTX 5070	11.94	\N	\N	0.111111	unavailable	https://console.vast.ai/console/create/	31.40	250.00	2026-07-22 19:09:21+00	4a4e3591-c6a7-4e5c-b09c-ffccd9a2fec5
unknown	gpu	RTX 4090	47.99	\N	\N	0.590370	unavailable	https://console.vast.ai/console/create/	125.90	450.00	2026-07-22 19:09:21+00	50157498-4201-45ae-b371-464a79cdf36c
unknown	gpu	RTX 5060 TI	15.93	\N	\N	0.054074	unavailable	https://console.vast.ai/console/create/	31.30	250.00	2026-07-22 19:09:21+00	505cccaa-0c7d-4310-8a7d-141387615e3f
unknown	gpu	RTX PRO 5000	47.79	\N	\N	1.280741	available	https://console.vast.ai/console/create/	251.90	250.00	2026-07-22 19:09:21+00	1ec48914-c37a-42d0-a647-7e9c9ec65cd1
unknown	gpu	RTX 5090	31.84	\N	\N	0.470370	available	https://console.vast.ai/console/create/	30.50	250.00	2026-07-22 19:09:21+00	dc103719-8178-4383-ab81-50a70e564484
unknown	gpu	RTX 5070	11.94	\N	\N	0.857778	unavailable	https://console.vast.ai/console/create/	251.50	250.00	2026-07-22 19:09:21+00	89ecd133-0aab-423e-99a3-365de367ef00
unknown	gpu	RTX 5090	31.84	\N	\N	2.241481	available	https://console.vast.ai/console/create/	503.50	250.00	2026-07-22 19:09:21+00	184dea67-cead-454e-aa8f-772ed033c4c3
unknown	gpu	H100 SXM	79.65	\N	\N	2.935556	unavailable	https://console.vast.ai/console/create/	431.90	700.00	2026-07-22 19:09:21+00	40d04818-e69d-4621-b349-515266414c90
unknown	gpu	H100 NVL	93.58	\N	\N	1.868889	unavailable	https://console.vast.ai/console/create/	314.70	700.00	2026-07-22 19:09:21+00	e3b8b079-5e4a-49bf-89f6-48726d8a123d
unknown	gpu	RTX PRO 4500	31.86	\N	\N	0.335556	unavailable	https://console.vast.ai/console/create/	188.60	250.00	2026-07-22 19:09:21+00	7363b113-ef51-40cd-ab6b-d21ba80a2a60
unknown	gpu	RTX 5090	31.84	\N	\N	0.470370	available	https://console.vast.ai/console/create/	30.50	250.00	2026-07-22 19:09:21+00	02c1a5db-6579-4a4e-a575-c976e1f3fa5d
unknown	gpu	RTX 4090	23.99	\N	\N	0.535556	unavailable	https://console.vast.ai/console/create/	125.70	450.00	2026-07-22 19:09:21+00	f20ef190-3a81-48bd-820d-fb4d7d3b26c5
unknown	gpu	RTX 4090	47.99	\N	\N	0.468889	available	https://console.vast.ai/console/create/	125.70	450.00	2026-07-22 19:09:21+00	64d3a5be-baac-4d8a-92f2-c2583f30167c
unknown	gpu	L4	22.49	\N	\N	0.032593	unavailable	https://console.vast.ai/console/create/	24.80	250.00	2026-07-22 19:09:21+00	d539809b-8ee6-44b0-9f9a-da1913b238f2
unknown	gpu	H100 NVL	93.58	\N	\N	4.369185	unavailable	https://console.vast.ai/console/create/	377.90	700.00	2026-07-22 19:09:21+00	fcadd2e6-36fe-4dd7-bf0d-0fcebb7a8a5e
unknown	gpu	RTX 5090	31.84	\N	\N	0.968721	available	https://console.vast.ai/console/create/	125.90	250.00	2026-07-22 19:09:21+00	052d1773-f9df-402d-948e-1c2c7af70912
unknown	gpu	RTX PRO 6000 S	95.59	\N	\N	2.669630	unavailable	https://console.vast.ai/console/create/	377.80	250.00	2026-07-22 19:09:21+00	13a108b7-04eb-44b6-9a02-ae4940384226
unknown	gpu	RTX 3090	24.00	\N	\N	0.121185	unavailable	https://console.vast.ai/console/create/	55.10	350.00	2026-07-22 19:09:21+00	2045c196-31dc-42f9-b513-793e3b8c21f9
unknown	gpu	H100 NVL	93.58	\N	\N	8.731852	unavailable	https://console.vast.ai/console/create/	755.80	700.00	2026-07-22 19:09:21+00	c6864a85-4292-4daa-95c6-4e7b2e557249
unknown	gpu	RTX PRO 6000 S	95.59	\N	\N	3.469630	available	https://console.vast.ai/console/create/	251.70	250.00	2026-07-22 19:09:21+00	e7258be7-ddc8-4be4-9898-220ce133305e
unknown	gpu	RTX PRO 6000 S	95.59	\N	\N	1.736296	unavailable	https://console.vast.ai/console/create/	125.90	250.00	2026-07-22 19:09:21+00	8bfa6b9c-97a6-466d-81ba-7ae0a392d3b0
unknown	gpu	RTX 5080	15.92	\N	\N	0.228889	unavailable	https://console.vast.ai/console/create/	30.90	250.00	2026-07-22 19:09:21+00	fd7262aa-fc76-4ecf-bfd1-4d7f13a23849
unknown	gpu	L40S	44.99	\N	\N	0.428593	unavailable	https://console.vast.ai/console/create/	118.10	350.00	2026-07-22 19:09:21+00	b51a6fd3-21f4-4fae-959e-ba34b2d8e6f0
unknown	gpu	RTX PRO 6000 S	95.59	\N	\N	1.736296	unavailable	https://console.vast.ai/console/create/	125.90	250.00	2026-07-22 19:09:21+00	b3a00f1f-5be5-4e8e-b820-15392fcf77d2
unknown	gpu	RTX PRO 6000 S	95.59	\N	\N	3.469630	unavailable	https://console.vast.ai/console/create/	251.90	250.00	2026-07-22 19:09:21+00	0567f8a9-1898-4d9c-82cc-df3ff44556e1
unknown	gpu	RTX 5080	15.92	\N	\N	0.351111	unavailable	https://console.vast.ai/console/create/	62.90	250.00	2026-07-22 19:09:21+00	0eb743f8-d744-4f28-9812-e2a81095a133
unknown	gpu	RTX PRO 6000 WS	95.59	\N	\N	5.305037	unavailable	https://console.vast.ai/console/create/	503.70	250.00	2026-07-22 19:09:21+00	6ea9e7a2-8df4-4c76-8d47-c2fa3cf66b2f
unknown	gpu	H200 NVL	140.40	\N	\N	2.610222	unavailable	https://console.vast.ai/console/create/	354.20	250.00	2026-07-22 19:09:21+00	f1168523-ff99-4000-beeb-7609448095d3
unknown	gpu	RTX 3090	24.00	\N	\N	0.241185	available	https://console.vast.ai/console/create/	110.10	350.00	2026-07-22 19:09:21+00	dd52ab47-6e6b-44ae-8b7a-9f42e5da6db3
unknown	gpu	RTX 5090	31.84	\N	\N	0.212889	unavailable	https://console.vast.ai/console/create/	62.60	250.00	2026-07-22 19:09:21+00	8dc06c20-9029-4d2f-b0d7-09ef5d97db08
unknown	gpu	RTX 4090	23.99	\N	\N	0.337778	unavailable	https://console.vast.ai/console/create/	108.10	450.00	2026-07-22 19:09:21+00	ce7b736a-45be-4c69-8e56-918558c2f7ed
unknown	gpu	RTX 5080	15.92	\N	\N	0.175111	unavailable	https://console.vast.ai/console/create/	27.50	250.00	2026-07-22 19:09:21+00	101f1e8f-6ab7-476c-b0ae-9b353c3cf455
unknown	gpu	RTX 5090	31.84	\N	\N	1.551852	unavailable	https://console.vast.ai/console/create/	251.90	250.00	2026-07-22 19:09:21+00	2bb509b1-e46f-4f9b-84b4-8d76b0e2c093
unknown	gpu	RTX PRO 4500	31.86	\N	\N	0.215556	unavailable	https://console.vast.ai/console/create/	503.80	250.00	2026-07-22 19:09:21+00	2131c42d-bd28-4baf-9c10-cb167a4aafd6
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.057778	unavailable	https://console.vast.ai/console/create/	62.80	250.00	2026-07-22 19:19:15+00	4acf1396-f17e-442c-9b09-04d9000af536
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.111111	unavailable	https://console.vast.ai/console/create/	125.60	250.00	2026-07-22 19:19:15+00	ce4a1ad5-eed6-4e86-969b-cb13c12532ae
vast-ai	gpu	TESLA V100	32.00	\N	\N	0.087556	unavailable	https://console.vast.ai/console/create/	125.50	300.00	2026-07-22 19:19:15+00	bcfd7914-a398-44af-9289-6a8aa2ac9165
vast-ai	gpu	TESLA V100	32.00	\N	\N	0.172889	unavailable	https://console.vast.ai/console/create/	251.10	300.00	2026-07-22 19:19:15+00	d7c99323-67c2-4d76-bad9-4bb26857a2e5
vast-ai	gpu	TESLA V100	32.00	\N	\N	0.042222	unavailable	https://console.vast.ai/console/create/	62.80	300.00	2026-07-22 19:19:15+00	9b48700f-c3f0-4bd6-af64-c9a47e9eba34
vast-ai	gpu	TESLA V100	32.00	\N	\N	0.020889	unavailable	https://console.vast.ai/console/create/	31.40	300.00	2026-07-22 19:19:15+00	36cfa6b0-22d5-43b8-92d2-5dda401d95f4
vast-ai	gpu	RTX PRO 6000 S	95.59	\N	\N	0.774756	unavailable	https://console.vast.ai/console/create/	124.80	250.00	2026-07-22 19:19:15+00	ef146c26-1c99-4c46-b3e4-acf34b938049
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.375556	unavailable	https://console.vast.ai/console/create/	62.80	250.00	2026-07-22 19:19:15+00	f94348bb-5d6e-4011-8b6f-625370b948af
vast-ai	gpu	RTX 5070 TI	15.92	\N	\N	0.095556	unavailable	https://console.vast.ai/console/create/	62.80	250.00	2026-07-22 19:19:15+00	b7161c7e-4753-4f79-a266-f5b1580ee444
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.457778	available	https://console.vast.ai/console/create/	70.80	250.00	2026-07-22 19:19:15+00	f18a7a0e-3a74-44d7-b436-49559512ab3e
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.911111	unavailable	https://console.vast.ai/console/create/	141.60	250.00	2026-07-22 19:19:15+00	79c2df39-842d-4520-a5d8-d1f72a748c9d
vast-ai	gpu	RTX PRO 6000 WS	95.59	\N	\N	1.003704	unavailable	https://console.vast.ai/console/create/	167.90	250.00	2026-07-22 19:19:15+00	36db9feb-9a95-4032-ae13-9390ee07a981
vast-ai	gpu	RTX PRO 6000 WS	95.59	\N	\N	0.736296	unavailable	https://console.vast.ai/console/create/	124.70	250.00	2026-07-22 19:19:15+00	09aea4b3-c1da-4e1b-a2fd-3212849d4e86
vast-ai	gpu	RTX PRO 6000 WS	95.59	\N	\N	2.135556	unavailable	https://console.vast.ai/console/create/	188.80	250.00	2026-07-22 19:19:15+00	b66d279d-5e98-4133-bcad-b20cab539b48
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.643704	unavailable	https://console.vast.ai/console/create/	125.70	250.00	2026-07-22 19:19:15+00	5d36a084-57ec-456d-b40f-aa136d62c868
vast-ai	gpu	RTX 4090	23.99	\N	\N	0.135556	available	https://console.vast.ai/console/create/	31.40	450.00	2026-07-22 19:19:15+00	bcdc108f-49a0-445c-b659-f8e31405269d
vast-ai	gpu	RTX 5070	11.94	\N	\N	0.431111	unavailable	https://console.vast.ai/console/create/	125.80	250.00	2026-07-22 19:19:15+00	7b493ac5-b400-4418-a139-d626f5b7ec27
vast-ai	gpu	RTX 4090	23.99	\N	\N	0.268889	unavailable	https://console.vast.ai/console/create/	62.90	450.00	2026-07-22 19:19:15+00	223f8dfc-ac41-4ec5-ba1f-9112366fad76
vast-ai	gpu	L4	22.49	\N	\N	0.021630	available	https://console.vast.ai/console/create/	21.90	250.00	2026-07-22 19:19:15+00	67152cba-3049-4eff-ac75-b583b7dc3b3c
vast-ai	gpu	RTX PRO 6000 S	95.59	\N	\N	1.202222	unavailable	https://console.vast.ai/console/create/	125.90	250.00	2026-07-22 19:19:15+00	71b129b9-13b7-445f-9cb6-7c685059f84e
vast-ai	gpu	RTX 5070	11.94	\N	\N	0.217778	unavailable	https://console.vast.ai/console/create/	62.90	250.00	2026-07-22 19:19:15+00	d934bb67-060b-45fe-81c2-a7a4cbbf9032
vast-ai	gpu	RTX 4090	23.99	\N	\N	0.182222	unavailable	https://console.vast.ai/console/create/	62.80	450.00	2026-07-22 19:19:15+00	593011b0-15c3-4db2-bc9c-75b1cd66eb87
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.403704	unavailable	https://console.vast.ai/console/create/	30.50	250.00	2026-07-22 19:19:15+00	61eca782-bcd5-47f4-bd62-1dcbb0e0cc80
vast-ai	gpu	RTX 4090	22.49	\N	\N	0.335556	available	https://console.vast.ai/console/create/	251.70	450.00	2026-07-22 19:19:15+00	1c4fd2d0-433f-4af4-9d4c-f8095e6de5cc
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.826222	available	https://console.vast.ai/console/create/	62.80	250.00	2026-07-22 19:19:15+00	245e1a55-eb05-4c89-a53b-746724a7edf9
vast-ai	gpu	RTX PRO 4500	31.86	\N	\N	0.335556	unavailable	https://console.vast.ai/console/create/	188.60	250.00	2026-07-22 19:19:15+00	dee3bcf7-7535-4f26-94b3-dd9bc15f5e28
vast-ai	gpu	RTX 4080S	15.99	\N	\N	0.098222	unavailable	https://console.vast.ai/console/create/	62.60	320.00	2026-07-22 19:19:15+00	f6cc701b-b300-489c-bb4e-50a3fd414d3a
vast-ai	gpu	RTX 5070 TI	15.92	\N	\N	0.135556	available	https://console.vast.ai/console/create/	62.60	250.00	2026-07-22 19:19:15+00	a5dcd972-5b7a-4166-bf5d-f051c28cd4f5
vast-ai	gpu	RTX PRO 6000 S	95.59	\N	\N	2.535556	unavailable	https://console.vast.ai/console/create/	251.90	250.00	2026-07-22 19:19:15+00	95a085fc-6b7d-4d49-a433-4bb9f2d7b391
vast-ai	gpu	RTX 4090	23.99	\N	\N	0.535556	unavailable	https://console.vast.ai/console/create/	125.70	450.00	2026-07-22 19:19:15+00	d0675585-f3d8-4e95-998b-e86a1821de82
vast-ai	gpu	RTX 5070	11.94	\N	\N	0.857778	unavailable	https://console.vast.ai/console/create/	251.50	250.00	2026-07-22 19:19:15+00	2f7f7cf6-f98d-4c1a-a164-1c542b07ef01
vast-ai	gpu	RTX 5080	15.92	\N	\N	0.155111	unavailable	https://console.vast.ai/console/create/	30.50	250.00	2026-07-22 19:19:15+00	cacf68a4-85b3-4697-bde5-b2eacf912386
vast-ai	gpu	RTX 4090	47.99	\N	\N	0.590370	unavailable	https://console.vast.ai/console/create/	125.90	450.00	2026-07-22 19:19:15+00	b1486b9b-2d5b-4fd9-855c-5bf44bdd59eb
vast-ai	gpu	H100 NVL	93.58	\N	\N	8.406519	unavailable	https://console.vast.ai/console/create/	755.80	700.00	2026-07-22 19:19:15+00	d1c2a409-3ac7-4f12-a1db-9460a7b0c929
vast-ai	gpu	RTX 5080	15.92	\N	\N	0.748889	unavailable	https://console.vast.ai/console/create/	62.20	250.00	2026-07-22 19:19:15+00	fb90e739-241e-4ec5-a65f-9c5649d75f78
vast-ai	gpu	RTX 5090	31.84	\N	\N	2.135556	unavailable	https://console.vast.ai/console/create/	125.80	250.00	2026-07-22 19:19:15+00	502b19df-466f-4ba9-a25c-596240346c13
vast-ai	gpu	RTX 5080	15.92	\N	\N	0.143452	unavailable	https://console.vast.ai/console/create/	92.20	250.00	2026-07-22 19:19:15+00	778c61f0-08e4-4f6f-bc28-f31967492673
vast-ai	gpu	RTX 5070 TI	15.92	\N	\N	0.135556	available	https://console.vast.ai/console/create/	31.30	250.00	2026-07-22 19:19:15+00	b56e9465-e226-4940-bc1e-145c7115e544
vast-ai	gpu	RTX PRO 6000 WS	95.59	\N	\N	1.329037	unavailable	https://console.vast.ai/console/create/	125.90	250.00	2026-07-22 19:19:15+00	52d0f082-16f6-4907-9037-a95c977e3cc6
vast-ai	gpu	RTX 5070	11.94	\N	\N	0.083704	available	https://console.vast.ai/console/create/	31.40	250.00	2026-07-22 19:19:15+00	cfae8d7d-f6dc-4f44-aa77-9ef150b3463e
vast-ai	gpu	RTX 5060 TI	15.93	\N	\N	0.054074	unavailable	https://console.vast.ai/console/create/	31.30	250.00	2026-07-22 19:19:15+00	f0241c9f-d02c-471e-8f23-fad6759a8f9d
vast-ai	gpu	RTX 4080S	15.99	\N	\N	0.098222	unavailable	https://console.vast.ai/console/create/	62.60	320.00	2026-07-22 19:19:15+00	3a97fefd-a51f-411a-b7a1-fae3b1d32de2
vast-ai	gpu	RTX 5090	31.84	\N	\N	1.334370	unavailable	https://console.vast.ai/console/create/	188.80	250.00	2026-07-22 19:19:15+00	7c78ccf9-1b43-4914-b47a-4082a931a8d7
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.468148	available	https://console.vast.ai/console/create/	62.80	250.00	2026-07-22 19:19:15+00	0171d080-63f3-4355-928a-c182ed299501
vast-ai	gpu	H100 NVL	93.58	\N	\N	4.206519	unavailable	https://console.vast.ai/console/create/	377.90	700.00	2026-07-22 19:19:15+00	4f70c30a-072d-4061-9b7c-0617b0a0e454
vast-ai	gpu	H100 SXM	79.65	\N	\N	4.402222	unavailable	https://console.vast.ai/console/create/	647.80	700.00	2026-07-22 19:19:15+00	e2200468-7ca3-4ed6-b587-67131f424121
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.212889	unavailable	https://console.vast.ai/console/create/	62.60	250.00	2026-07-22 19:19:15+00	8574a800-349d-4867-9ae7-955e54d6484c
vast-ai	gpu	H100 NVL	93.58	\N	\N	16.806519	unavailable	https://console.vast.ai/console/create/	1511.50	700.00	2026-07-22 19:19:15+00	86b8bbc1-50ae-4f43-9813-951c084a488c
vast-ai	gpu	RTX PRO 6000 WS	95.59	\N	\N	2.671852	unavailable	https://console.vast.ai/console/create/	188.90	250.00	2026-07-22 19:19:15+00	55fe3877-84e3-487a-98f2-4834c0f7b939
vast-ai	gpu	RTX 5070 TI	15.92	\N	\N	0.322963	unavailable	https://console.vast.ai/console/create/	62.60	250.00	2026-07-22 19:19:15+00	f5951b67-7c3c-4994-8736-29033152b29a
vast-ai	gpu	RTX 5080	15.92	\N	\N	0.242222	unavailable	https://console.vast.ai/console/create/	110.00	250.00	2026-07-22 19:19:15+00	7276df83-4a2f-42b6-a9ac-169fea8c4745
vast-ai	gpu	RTX 5080	15.92	\N	\N	0.345778	unavailable	https://console.vast.ai/console/create/	55.00	250.00	2026-07-22 19:19:15+00	0b3aa9fa-9487-4341-b258-fa12e0b93572
vast-ai	gpu	RTX 5070 TI	15.92	\N	\N	0.537037	unavailable	https://console.vast.ai/console/create/	125.70	250.00	2026-07-22 19:19:15+00	d07c3647-cc68-4ec2-b013-1df5b2046545
vast-ai	gpu	RTX 4090	47.99	\N	\N	0.935556	unavailable	https://console.vast.ai/console/create/	251.40	450.00	2026-07-22 19:19:15+00	8cb5db23-0c7d-49bb-bff2-2d1bf429d33d
vast-ai	gpu	H200 NVL	140.40	\N	\N	2.610222	unavailable	https://console.vast.ai/console/create/	354.20	250.00	2026-07-22 19:19:15+00	4675b0b0-c320-4762-b691-beb9576232bc
vast-ai	gpu	RTX PRO 6000 S	95.59	\N	\N	1.736296	unavailable	https://console.vast.ai/console/create/	125.90	250.00	2026-07-22 19:19:15+00	2d56bad4-483b-4f90-a9b1-6bd365257d37
vast-ai	gpu	RTX 3090	24.00	\N	\N	0.121185	available	https://console.vast.ai/console/create/	55.10	350.00	2026-07-22 19:19:15+00	21353122-d40a-4aab-9868-613a2985948f
vast-ai	gpu	RTX PRO 6000 WS	95.59	\N	\N	8.535556	unavailable	https://console.vast.ai/console/create/	755.40	250.00	2026-07-22 19:19:15+00	8468d659-2717-4429-9c1c-f271de97bfda
vast-ai	gpu	RTX PRO 5000	47.79	\N	\N	2.560074	available	https://console.vast.ai/console/create/	251.70	250.00	2026-07-22 19:19:15+00	133092f8-f295-441e-8400-b0d85134be1e
vast-ai	gpu	RTX 3090	24.00	\N	\N	0.078222	available	https://console.vast.ai/console/create/	31.40	350.00	2026-07-22 19:19:15+00	a16069a6-57b8-477e-b08f-281963c8d76e
vast-ai	gpu	RTX 6000ADA	47.99	\N	\N	0.772889	unavailable	https://console.vast.ai/console/create/	167.90	250.00	2026-07-22 19:19:15+00	272ce2a9-1699-4fe1-a866-20bb54a518a2
vast-ai	gpu	RTX 4090	23.99	\N	\N	0.352593	unavailable	https://console.vast.ai/console/create/	117.90	450.00	2026-07-22 19:19:15+00	04865a01-ce78-4f47-88cb-86a947653699
vast-ai	gpu	RTX 4090	47.99	\N	\N	0.564444	unavailable	https://console.vast.ai/console/create/	94.40	450.00	2026-07-22 19:19:15+00	8be2fe0e-c054-439d-97d2-6a0f20f9987f
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.470370	available	https://console.vast.ai/console/create/	30.50	250.00	2026-07-22 19:19:15+00	c6138933-6a74-4b82-b4e0-1aae3fe78cc1
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.057778	available	https://console.vast.ai/console/create/	62.80	250.00	2026-07-22 19:33:45+00	cca739b9-817d-4860-9388-b747dcd0efc6
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.111111	unavailable	https://console.vast.ai/console/create/	125.60	250.00	2026-07-22 19:33:45+00	c85793d2-9a8b-4a40-8d68-b694b581643c
vast-ai	gpu	TESLA V100	32.00	\N	\N	0.076889	unavailable	https://console.vast.ai/console/create/	125.50	300.00	2026-07-22 19:33:45+00	d5087dc3-9e98-45e6-8e8a-663727b8c3ad
vast-ai	gpu	TESLA V100	32.00	\N	\N	0.151556	unavailable	https://console.vast.ai/console/create/	251.10	300.00	2026-07-22 19:33:45+00	156f4828-d4ba-4f43-87b6-1342f7d91599
vast-ai	gpu	TESLA V100	32.00	\N	\N	0.020889	unavailable	https://console.vast.ai/console/create/	31.40	300.00	2026-07-22 19:33:45+00	234a9322-6a74-472a-80d1-7567bc040991
vast-ai	gpu	TESLA V100	32.00	\N	\N	0.050222	unavailable	https://console.vast.ai/console/create/	62.80	300.00	2026-07-22 19:33:45+00	ac9377b4-7baa-4e36-a99d-3471c65015b5
vast-ai	gpu	RTX PRO 6000 S	95.59	\N	\N	0.774756	unavailable	https://console.vast.ai/console/create/	124.80	250.00	2026-07-22 19:33:45+00	42dec425-ac24-4c0c-b374-d5ce8b313493
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.294815	unavailable	https://console.vast.ai/console/create/	63.00	250.00	2026-07-22 19:33:45+00	2f87a85f-3fe7-40da-8dcd-20ac0a476259
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.911111	unavailable	https://console.vast.ai/console/create/	141.60	250.00	2026-07-22 19:33:45+00	c5ca305b-bef7-4d88-b6bd-c03a1e99b861
vast-ai	gpu	RTX PRO 6000 WS	95.59	\N	\N	1.868148	unavailable	https://console.vast.ai/console/create/	251.20	250.00	2026-07-22 19:33:45+00	8b68c15f-42f7-402a-8c91-a668e2380a9d
vast-ai	gpu	RTX PRO 6000 WS	95.59	\N	\N	0.734815	unavailable	https://console.vast.ai/console/create/	126.00	250.00	2026-07-22 19:33:45+00	406cde07-ecac-4f25-9900-bca2fa72a034
vast-ai	gpu	RTX 4070S TI	15.99	\N	\N	0.080296	unavailable	https://console.vast.ai/console/create/	62.70	250.00	2026-07-22 19:33:45+00	183f7b52-3199-4e7c-9444-78e6e6b520c1
vast-ai	gpu	RTX PRO 6000 WS	95.59	\N	\N	0.935556	available	https://console.vast.ai/console/create/	125.60	250.00	2026-07-22 19:33:45+00	f0646360-9f9e-4558-a548-7e55cd23c8e6
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.748889	unavailable	https://console.vast.ai/console/create/	125.60	250.00	2026-07-22 19:33:45+00	06826738-d78a-4be9-808f-b6f09b49c267
vast-ai	gpu	RTX PRO 6000 WS	95.59	\N	\N	1.682222	unavailable	https://console.vast.ai/console/create/	345.90	250.00	2026-07-22 19:33:45+00	98799714-9eec-4955-9074-5d3505c15323
vast-ai	gpu	RTX 4090	23.99	\N	\N	0.135556	available	https://console.vast.ai/console/create/	31.40	450.00	2026-07-22 19:33:45+00	29675b8f-6703-4ecb-a8df-d23a6782deb4
vast-ai	gpu	RTX 4090	23.99	\N	\N	0.268889	unavailable	https://console.vast.ai/console/create/	62.90	450.00	2026-07-22 19:33:45+00	cd529a48-55e1-44fa-b70f-e127a8aa0184
vast-ai	gpu	RTX 4080S	15.99	\N	\N	0.093481	unavailable	https://console.vast.ai/console/create/	62.60	320.00	2026-07-22 19:33:45+00	2baaddf6-80ff-46a8-a962-0928691d1bee
vast-ai	gpu	RTX 5070	11.94	\N	\N	0.431111	unavailable	https://console.vast.ai/console/create/	125.80	250.00	2026-07-22 19:33:45+00	5c76fbf0-3d30-4f57-81ff-0b1a013cf17c
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.414222	available	https://console.vast.ai/console/create/	31.40	250.00	2026-07-22 19:33:45+00	213d352a-68da-4468-bc43-b5ea725e553c
vast-ai	gpu	L4	22.49	\N	\N	0.021630	available	https://console.vast.ai/console/create/	21.90	250.00	2026-07-22 19:33:45+00	959c0202-1286-481f-b70f-2a084a94bc25
vast-ai	gpu	H100 SXM	79.65	\N	\N	1.468889	unavailable	https://console.vast.ai/console/create/	215.90	700.00	2026-07-22 19:33:45+00	9edc1adb-1896-4619-80e6-bb5b8d67ac0e
vast-ai	gpu	RTX 4090	23.99	\N	\N	0.182222	unavailable	https://console.vast.ai/console/create/	62.80	450.00	2026-07-22 19:33:45+00	1e364416-c8aa-42da-8cde-5bf87739eaa5
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.350370	unavailable	https://console.vast.ai/console/create/	63.00	250.00	2026-07-22 19:33:45+00	371ed57a-01ef-46b8-8895-cfb0fd0ac41f
vast-ai	gpu	RTX 4090	47.99	\N	\N	0.297037	unavailable	https://console.vast.ai/console/create/	62.90	450.00	2026-07-22 19:33:45+00	5aeef977-805f-453d-bcd2-3210637b6c66
vast-ai	gpu	H100 SXM	79.65	\N	\N	2.935556	unavailable	https://console.vast.ai/console/create/	431.90	700.00	2026-07-22 19:33:45+00	1a58b815-0c45-4f49-931a-f0c2e4c408dd
vast-ai	gpu	RTX 5070	11.94	\N	\N	0.217778	unavailable	https://console.vast.ai/console/create/	62.90	250.00	2026-07-22 19:33:45+00	0e229c37-e952-4fcf-8703-c2ca6385ec0d
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.403704	unavailable	https://console.vast.ai/console/create/	30.50	250.00	2026-07-22 19:33:45+00	d6406c59-6f12-4a51-ab8c-1d7a6f0fe48d
vast-ai	gpu	RTX PRO 6000 S	95.59	\N	\N	2.402222	unavailable	https://console.vast.ai/console/create/	251.90	250.00	2026-07-22 19:33:45+00	1152b848-77b2-465d-9d96-156a80a20baf
vast-ai	gpu	RTX 5070 TI	15.92	\N	\N	0.135556	unavailable	https://console.vast.ai/console/create/	31.30	250.00	2026-07-22 19:33:45+00	0a8af7fd-6dff-4aad-b571-672a5a86bf38
vast-ai	gpu	RTX 5080	15.92	\N	\N	0.143452	unavailable	https://console.vast.ai/console/create/	92.20	250.00	2026-07-22 19:33:45+00	dc953f99-12a0-4d78-b1d6-357b381a5caf
vast-ai	gpu	RTX PRO 4500	31.86	\N	\N	0.335556	available	https://console.vast.ai/console/create/	188.60	250.00	2026-07-22 19:33:45+00	d43002e2-4d4e-4457-9899-661ab0e42d96
vast-ai	gpu	RTX PRO 5000	47.79	\N	\N	1.280074	available	https://console.vast.ai/console/create/	125.80	250.00	2026-07-22 19:33:45+00	65f221b8-61d5-4b58-b2a3-14ccdbba08cc
vast-ai	gpu	RTX 5070 TI	15.92	\N	\N	0.135556	available	https://console.vast.ai/console/create/	31.30	250.00	2026-07-22 19:33:45+00	d3507168-1686-4a81-acc4-9653c136b99d
vast-ai	gpu	RTX PRO 6000 WS	95.59	\N	\N	2.654370	unavailable	https://console.vast.ai/console/create/	251.80	250.00	2026-07-22 19:33:45+00	0fa5b1ef-ab6a-4d08-adc0-7dd2a64ca6fe
vast-ai	gpu	RTX PRO 6000 WS	95.59	\N	\N	1.329037	unavailable	https://console.vast.ai/console/create/	125.90	250.00	2026-07-22 19:33:45+00	05e78463-1ee3-4653-99ca-7bce2be1b8c1
vast-ai	gpu	RTX 4090	23.99	\N	\N	0.535556	unavailable	https://console.vast.ai/console/create/	125.70	450.00	2026-07-22 19:33:45+00	632b4b89-4bd8-48d7-844a-568671560f48
vast-ai	gpu	RTX 4090	23.99	\N	\N	0.162222	unavailable	https://console.vast.ai/console/create/	125.70	450.00	2026-07-22 19:33:45+00	6696946c-4928-42c8-9adc-c77f8b27c1d2
vast-ai	gpu	RTX 5090	31.84	\N	\N	1.307704	unavailable	https://console.vast.ai/console/create/	188.80	250.00	2026-07-22 19:33:45+00	8502d5fd-13f3-41bf-9b40-49a8efe90e63
vast-ai	gpu	H100 NVL	93.58	\N	\N	1.842222	unavailable	https://console.vast.ai/console/create/	314.70	700.00	2026-07-22 19:33:45+00	b1a5a5ca-b574-4c0c-9c28-257a222cd3c3
vast-ai	gpu	RTX PRO 6000 S	95.59	\N	\N	3.469630	unavailable	https://console.vast.ai/console/create/	251.90	250.00	2026-07-22 19:33:45+00	e7d4435b-ef1b-42ca-86e0-8d2263463045
vast-ai	gpu	RTX PRO 6000 S	95.59	\N	\N	1.736296	unavailable	https://console.vast.ai/console/create/	125.90	250.00	2026-07-22 19:33:45+00	5a8977e2-451c-4fdf-9e31-90f6bc40a56e
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.470370	available	https://console.vast.ai/console/create/	30.50	250.00	2026-07-22 19:33:45+00	1a720858-e46b-4f1d-ab0a-f7f87ee1356e
vast-ai	gpu	RTX 5080	15.92	\N	\N	0.351111	unavailable	https://console.vast.ai/console/create/	62.90	250.00	2026-07-22 19:33:45+00	58b23a24-f3da-4e1a-985b-ab7f6f0688f2
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.854815	unavailable	https://console.vast.ai/console/create/	125.90	250.00	2026-07-22 19:33:45+00	dbca3c87-be68-47f2-8b24-05a53a648c15
vast-ai	gpu	RTX PRO 5000	47.79	\N	\N	2.560074	available	https://console.vast.ai/console/create/	251.70	250.00	2026-07-22 19:33:45+00	56f8f005-cf30-4903-b6c4-f6e47d0b9226
vast-ai	gpu	RTX 5070 TI	15.92	\N	\N	0.537037	unavailable	https://console.vast.ai/console/create/	125.70	250.00	2026-07-22 19:33:45+00	acc6a3ec-97e5-4e9e-b627-acb6066b0ead
vast-ai	gpu	RTX 5080	15.92	\N	\N	0.177778	unavailable	https://console.vast.ai/console/create/	31.40	250.00	2026-07-22 19:33:45+00	daccaefe-0c2c-4906-bd63-8f59fe4525ad
vast-ai	gpu	RTX 5070	11.94	\N	\N	0.090370	unavailable	https://console.vast.ai/console/create/	31.40	250.00	2026-07-22 19:33:45+00	12934200-e43c-4cc3-8087-e1d26cd9f87d
vast-ai	gpu	H200 NVL	140.40	\N	\N	2.610222	unavailable	https://console.vast.ai/console/create/	354.20	250.00	2026-07-22 19:33:45+00	d6f1cf70-7044-446b-9193-4a99016c6810
vast-ai	gpu	H200 NVL	140.40	\N	\N	1.522222	unavailable	https://console.vast.ai/console/create/	503.70	250.00	2026-07-22 19:33:45+00	dcc3e554-6bd4-4a47-aaff-f07fda15c01a
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.212889	unavailable	https://console.vast.ai/console/create/	62.60	250.00	2026-07-22 19:33:45+00	d7624231-68af-49b9-8f04-e0cb328d6a23
vast-ai	gpu	RTX PRO 6000 S	95.59	\N	\N	1.200074	unavailable	https://console.vast.ai/console/create/	251.70	250.00	2026-07-22 19:33:45+00	f38584e1-e898-4dc9-8e57-a82f59f6f2af
vast-ai	gpu	RTX 6000ADA	47.99	\N	\N	0.387556	unavailable	https://console.vast.ai/console/create/	83.90	250.00	2026-07-22 19:33:45+00	8bec541d-2ff1-4672-b807-0c5bd7b1e4a2
vast-ai	gpu	RTX 5070	11.94	\N	\N	0.054815	unavailable	https://console.vast.ai/console/create/	62.90	250.00	2026-07-22 19:33:45+00	3cb91b6d-ffe1-41fe-82e8-cb090c2849a3
vast-ai	gpu	RTX 5080	15.92	\N	\N	0.280741	available	https://console.vast.ai/console/create/	251.50	250.00	2026-07-22 19:33:45+00	2877560b-0887-476f-aa17-543eeac2ab9a
vast-ai	gpu	RTX 5070	11.94	\N	\N	0.068444	available	https://console.vast.ai/console/create/	15.50	250.00	2026-07-22 19:33:45+00	096239d3-d5a0-4457-8985-a5e70452d557
vast-ai	gpu	RTX 5070 TI	15.92	\N	\N	0.268889	available	https://console.vast.ai/console/create/	62.60	250.00	2026-07-22 19:33:45+00	c85a696b-391a-492b-81c2-fc4a4580375e
vast-ai	gpu	RTX PRO 4500	31.86	\N	\N	0.215556	unavailable	https://console.vast.ai/console/create/	503.80	250.00	2026-07-22 19:33:45+00	1711c05c-3375-4143-879a-0cf3f2df5ae6
vast-ai	gpu	RTX 3090	24.00	\N	\N	0.222963	unavailable	https://console.vast.ai/console/create/	62.90	350.00	2026-07-22 19:33:45+00	921db137-fd53-4f80-8fdc-d509af958653
vast-ai	gpu	RTX PRO 6000 S	95.59	\N	\N	5.336296	unavailable	https://console.vast.ai/console/create/	755.70	250.00	2026-07-22 19:33:45+00	8b95b484-bb1a-4dfa-bfaf-69e80ce40e0a
vast-ai	gpu	RTX 4090D	47.99	\N	\N	0.402963	unavailable	https://console.vast.ai/console/create/	94.20	450.00	2026-07-22 19:33:45+00	75a05f79-abe8-490d-89ca-b3ce9d07aa27
vast-ai	gpu	RTX 5090	31.84	\N	\N	3.737778	unavailable	https://console.vast.ai/console/create/	755.50	250.00	2026-07-22 19:33:45+00	4ef2aac5-08f4-4377-b272-b4b27c44c39e
vast-ai	gpu	RTX 4090	23.99	\N	\N	0.724444	unavailable	https://console.vast.ai/console/create/	201.50	450.00	2026-07-22 19:33:45+00	732c2195-f582-4f33-b8c1-2053e624330a
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.057778	available	https://console.vast.ai/console/create/	62.80	250.00	2026-07-23 09:22:57+00	1d296471-b955-4151-9379-747035c1bfd9
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.111111	unavailable	https://console.vast.ai/console/create/	125.60	250.00	2026-07-23 09:22:57+00	b6524bb6-9b2d-4e27-85bd-9991e299df2c
vast-ai	gpu	TESLA V100	32.00	\N	\N	0.151556	unavailable	https://console.vast.ai/console/create/	188.10	300.00	2026-07-23 09:22:57+00	449c2a95-8e96-4422-b52c-3ad05d2ab760
vast-ai	gpu	TESLA V100	32.00	\N	\N	0.076889	unavailable	https://console.vast.ai/console/create/	125.50	300.00	2026-07-23 09:22:57+00	8fe4d850-5d3b-422c-adf1-034356aff3f2
vast-ai	gpu	TESLA V100	32.00	\N	\N	0.039556	unavailable	https://console.vast.ai/console/create/	62.80	300.00	2026-07-23 09:22:57+00	dcb16a98-a316-42d3-b1af-d972d549e4e1
vast-ai	gpu	TESLA V100	32.00	\N	\N	0.020889	unavailable	https://console.vast.ai/console/create/	31.40	300.00	2026-07-23 09:22:57+00	1aad3bd9-109e-4f8a-a745-ea41a7d41c35
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.308148	unavailable	https://console.vast.ai/console/create/	63.00	250.00	2026-07-23 09:22:57+00	744afc94-b44d-4f9b-810e-9da77a188f8e
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.281481	available	https://console.vast.ai/console/create/	63.00	250.00	2026-07-23 09:22:57+00	b9597eab-7b5c-4f01-a1d2-d398e3cd43a1
vast-ai	gpu	RTX PRO 6000 WS	95.59	\N	\N	1.002222	available	https://console.vast.ai/console/create/	251.90	250.00	2026-07-23 09:22:57+00	c436bb96-3e7e-4d10-b7e5-404284684f94
vast-ai	gpu	RTX 4090	23.99	\N	\N	0.168889	available	https://console.vast.ai/console/create/	125.90	450.00	2026-07-23 09:22:57+00	f2741f1f-73e9-4c6d-804b-f9de33d66cb1
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.622963	unavailable	https://console.vast.ai/console/create/	125.90	250.00	2026-07-23 09:22:57+00	445b3d21-c7d2-4f23-9df3-db4245927654
vast-ai	gpu	RTX 5070 TI	15.92	\N	\N	0.188889	unavailable	https://console.vast.ai/console/create/	125.60	250.00	2026-07-23 09:22:57+00	4474aa04-a61d-41b3-a4fc-399cc62ed07e
vast-ai	gpu	RTX 4070S TI	15.99	\N	\N	0.080296	unavailable	https://console.vast.ai/console/create/	62.60	250.00	2026-07-23 09:22:57+00	d2535be2-a169-41f4-a0e4-95e6aac1de04
vast-ai	gpu	RTX PRO 6000 WS	95.59	\N	\N	2.187704	unavailable	https://console.vast.ai/console/create/	377.30	250.00	2026-07-23 09:22:57+00	3b79e0dc-7c22-4f6c-be53-dfaf4bc742c8
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.350370	unavailable	https://console.vast.ai/console/create/	63.00	250.00	2026-07-23 09:22:57+00	c583daeb-ff2b-40de-aea1-528f82f7fa20
vast-ai	gpu	RTX 4090	23.99	\N	\N	0.268889	available	https://console.vast.ai/console/create/	62.90	450.00	2026-07-23 09:22:57+00	6672d42c-179a-4879-bf81-e3ab122f7496
vast-ai	gpu	RTX 5070	11.94	\N	\N	0.431111	unavailable	https://console.vast.ai/console/create/	125.80	250.00	2026-07-23 09:22:57+00	774f64d4-a61e-4222-9377-4917b41ffe2d
vast-ai	gpu	RTX 4090	23.99	\N	\N	0.135556	available	https://console.vast.ai/console/create/	31.40	450.00	2026-07-23 09:22:57+00	f6d8236a-1c70-49f6-8a26-a561d5091005
vast-ai	gpu	RTX PRO 6000 WS	95.59	\N	\N	1.002222	available	https://console.vast.ai/console/create/	179.90	250.00	2026-07-23 09:22:57+00	da85cbdb-1ebd-4011-b307-2385a3e66f8b
vast-ai	gpu	H100 SXM	79.65	\N	\N	1.468889	unavailable	https://console.vast.ai/console/create/	215.90	700.00	2026-07-23 09:22:57+00	6bbaca7c-774d-4806-9d31-3788ae0479fe
vast-ai	gpu	RTX 5070 TI	15.92	\N	\N	0.214815	unavailable	https://console.vast.ai/console/create/	60.70	250.00	2026-07-23 09:22:57+00	db45db34-36dc-4851-9752-dd4210c79b1e
vast-ai	gpu	RTX 4080S	15.99	\N	\N	0.093630	unavailable	https://console.vast.ai/console/create/	62.60	320.00	2026-07-23 09:22:57+00	bf31cb3c-850e-4e93-ade0-49eccd21a4fe
vast-ai	gpu	RTX 5090	31.84	\N	\N	1.337037	unavailable	https://console.vast.ai/console/create/	212.40	250.00	2026-07-23 09:22:57+00	7707dd85-0c24-4dd6-85d2-92e363dafe8d
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.403704	unavailable	https://console.vast.ai/console/create/	30.50	250.00	2026-07-23 09:22:57+00	b7e794dd-0858-4bff-95e7-fc8c12c45ea6
vast-ai	gpu	RTX 5070	11.94	\N	\N	0.217778	unavailable	https://console.vast.ai/console/create/	62.90	250.00	2026-07-23 09:22:57+00	1d331e3f-e6d8-4689-8f2e-02b4bf6c71e6
vast-ai	gpu	RTX PRO 6000 S	95.59	\N	\N	1.268889	unavailable	https://console.vast.ai/console/create/	125.90	250.00	2026-07-23 09:22:57+00	c7766459-2b0e-4c17-b2eb-5efcf25248dd
vast-ai	gpu	RTX 5070 TI	15.92	\N	\N	0.135556	available	https://console.vast.ai/console/create/	31.30	250.00	2026-07-23 09:22:57+00	08a2f6b8-98f8-4815-9677-0c696e2894cc
vast-ai	gpu	RTX 4080S	15.99	\N	\N	0.098222	unavailable	https://console.vast.ai/console/create/	62.60	320.00	2026-07-23 09:22:57+00	0beecba5-5bd7-4e32-a763-b44d37e0b1d7
vast-ai	gpu	RTX 5090	31.84	\N	\N	1.068148	available	https://console.vast.ai/console/create/	157.20	250.00	2026-07-23 09:22:57+00	69a25f6d-7871-4023-ac0e-a302dcfc236a
vast-ai	gpu	RTX 4090	47.99	\N	\N	0.590370	unavailable	https://console.vast.ai/console/create/	125.90	450.00	2026-07-23 09:22:57+00	eb1e72e6-c8a9-4129-a297-fdf89f144199
vast-ai	gpu	H100 NVL	93.58	\N	\N	1.868148	unavailable	https://console.vast.ai/console/create/	314.70	700.00	2026-07-23 09:22:57+00	51d657b7-e766-49af-84ad-6cf0e2d68cca
vast-ai	gpu	RTX 4090	23.99	\N	\N	0.535556	unavailable	https://console.vast.ai/console/create/	125.70	450.00	2026-07-23 09:22:57+00	1741c47f-f005-460b-b45f-40188d0ed72a
vast-ai	gpu	RTX 5070 TI	15.92	\N	\N	0.135556	unavailable	https://console.vast.ai/console/create/	31.00	250.00	2026-07-23 09:22:57+00	79bca328-5846-4419-9eeb-cc92cb4aeda2
vast-ai	gpu	RTX 5070	11.94	\N	\N	0.110370	unavailable	https://console.vast.ai/console/create/	41.90	250.00	2026-07-23 09:22:57+00	6521b88f-0257-4ff8-9143-ceba9c4d72e5
vast-ai	gpu	RTX 5080	15.92	\N	\N	0.162222	unavailable	https://console.vast.ai/console/create/	31.30	250.00	2026-07-23 09:22:57+00	fa61b0e2-eb4a-4a6c-be6e-d1e6db784ffd
vast-ai	gpu	RTX 5070	11.94	\N	\N	0.857778	unavailable	https://console.vast.ai/console/create/	251.50	250.00	2026-07-23 09:22:57+00	4c73a709-1757-42ff-85f6-3abb48538368
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.470370	unavailable	https://console.vast.ai/console/create/	30.50	250.00	2026-07-23 09:22:57+00	8da92fda-4998-45be-bbbd-3060b8c9dd5a
vast-ai	gpu	RTX PRO 4500	31.86	\N	\N	0.335556	unavailable	https://console.vast.ai/console/create/	188.60	250.00	2026-07-23 09:22:57+00	3680a630-d214-4406-a959-c098753f2196
vast-ai	gpu	RTX 5060 TI	15.93	\N	\N	0.150370	unavailable	https://console.vast.ai/console/create/	62.80	250.00	2026-07-23 09:22:57+00	c34de4fb-a8b3-48d1-8f45-46c41889a389
vast-ai	gpu	RTX 6000ADA	47.99	\N	\N	0.350222	unavailable	https://console.vast.ai/console/create/	83.90	250.00	2026-07-23 09:22:57+00	83064196-4434-40fa-b5bb-23201921f99b
vast-ai	gpu	RTX 4090	47.99	\N	\N	0.935556	unavailable	https://console.vast.ai/console/create/	251.40	450.00	2026-07-23 09:22:57+00	37889407-3ad7-42a0-89a8-b38371fdc1b0
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.212889	unavailable	https://console.vast.ai/console/create/	62.60	250.00	2026-07-23 09:22:57+00	55f8711f-b136-4469-9c8d-90ecfc08369d
vast-ai	gpu	RTX 5080	15.92	\N	\N	0.162222	available	https://console.vast.ai/console/create/	31.30	250.00	2026-07-23 09:22:57+00	1f55dc90-140b-49a6-acb4-832856db452c
vast-ai	gpu	RTX 6000ADA	47.99	\N	\N	0.698222	unavailable	https://console.vast.ai/console/create/	167.90	250.00	2026-07-23 09:22:57+00	78c80654-31d0-46f9-9dce-89b322782a68
vast-ai	gpu	RTX PRO 6000 S	95.59	\N	\N	1.736296	available	https://console.vast.ai/console/create/	125.90	250.00	2026-07-23 09:22:57+00	9f110163-6a89-44b2-970a-c6d5a3aa7412
vast-ai	gpu	RTX PRO 6000 S	95.59	\N	\N	3.469630	unavailable	https://console.vast.ai/console/create/	251.70	250.00	2026-07-23 09:22:57+00	3de62c1a-eed5-46c1-a5fc-748230c779f2
vast-ai	gpu	RTX 4090	23.99	\N	\N	0.321407	unavailable	https://console.vast.ai/console/create/	125.60	450.00	2026-07-23 09:22:57+00	0fab4ed5-f9ed-47f0-952b-1aee845a1c4c
vast-ai	gpu	L40S	44.99	\N	\N	0.855259	unavailable	https://console.vast.ai/console/create/	236.10	350.00	2026-07-23 09:22:57+00	eacf7f45-9222-4ed4-ac65-9755546c2a74
vast-ai	gpu	RTX 5090	31.84	\N	\N	1.202222	unavailable	https://console.vast.ai/console/create/	125.90	250.00	2026-07-23 09:22:57+00	a1602d82-8150-4b2b-80a3-33785cb8d349
vast-ai	gpu	RTX 5080	15.92	\N	\N	0.267407	available	https://console.vast.ai/console/create/	251.50	250.00	2026-07-23 09:22:57+00	2b46c14e-368f-41b2-953a-a6af7dd788c0
vast-ai	gpu	RTX PRO 6000 WS	95.59	\N	\N	5.305037	unavailable	https://console.vast.ai/console/create/	503.70	250.00	2026-07-23 09:22:57+00	988202db-c49b-4421-baad-ba932e77bee1
vast-ai	gpu	RTX PRO 6000 S	95.59	\N	\N	2.669630	unavailable	https://console.vast.ai/console/create/	377.80	250.00	2026-07-23 09:22:57+00	69c26add-8021-403d-85e5-66ba2129d866
vast-ai	gpu	RTX PRO 6000 WS	95.59	\N	\N	3.068148	unavailable	https://console.vast.ai/console/create/	125.90	250.00	2026-07-23 09:22:57+00	20d88aee-333b-408a-a01e-3aae943d7847
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.935556	available	https://console.vast.ai/console/create/	100.60	250.00	2026-07-23 09:22:57+00	7dd54964-2f90-4dd0-9378-28f58976fd3b
vast-ai	gpu	RTX 3090	24.00	\N	\N	0.122222	available	https://console.vast.ai/console/create/	31.50	350.00	2026-07-23 09:22:57+00	abe20a7b-5263-4775-9341-6e17116843cb
vast-ai	gpu	RTX 3090	24.00	\N	\N	0.162222	unavailable	https://console.vast.ai/console/create/	62.80	350.00	2026-07-23 09:22:57+00	06a60b1b-d8cf-4d49-b4a4-31ab9047cab9
vast-ai	gpu	RTX PRO 6000 WS	95.59	\N	\N	1.338519	available	https://console.vast.ai/console/create/	94.40	250.00	2026-07-23 09:22:57+00	913264ad-f774-48b0-adc8-397afee304c1
vast-ai	gpu	RTX 5080	15.92	\N	\N	0.345778	unavailable	https://console.vast.ai/console/create/	55.00	250.00	2026-07-23 09:22:57+00	5e9dea99-4e69-4bbe-ba0f-c07e7f01d70d
vast-ai	gpu	RTX 5070 TI	15.92	\N	\N	0.537037	unavailable	https://console.vast.ai/console/create/	125.70	250.00	2026-07-23 09:22:57+00	73500a64-a6a7-42a2-b63c-61e765b801be
vast-ai	gpu	RTX 3080 TI	12.00	\N	\N	0.154222	unavailable	https://console.vast.ai/console/create/	30.60	320.00	2026-07-23 09:22:57+00	65ab4169-9560-4407-b4a5-ce2fb768c49f
vast-ai	gpu	H200 NVL	140.40	\N	\N	2.611111	unavailable	https://console.vast.ai/console/create/	354.20	250.00	2026-07-23 09:22:57+00	85bc15a4-785c-45b5-8b7e-32f4dae0175a
vast-ai	gpu	RTX PRO 6000 S	95.59	\N	\N	5.557037	unavailable	https://console.vast.ai/console/create/	755.70	250.00	2026-07-23 09:22:57+00	9eb14740-4c29-4486-b798-e36ab59939e9
vast-ai	gpu	RTX 4090D	23.99	\N	\N	0.388148	unavailable	https://console.vast.ai/console/create/	125.90	450.00	2026-07-23 09:22:57+00	06190427-cc9d-4aa6-bf18-3618b0e8937d
vast-ai	gpu	RTX 4090	47.99	\N	\N	0.537778	unavailable	https://console.vast.ai/console/create/	125.90	450.00	2026-07-23 09:22:57+00	17206704-1849-4b32-84a0-7c19d41c3f3e
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.057778	unavailable	https://console.vast.ai/console/create/	62.80	250.00	2026-07-23 09:30:56+00	a55057d6-8e23-4028-afd2-6e1e0f22a6c8
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.111111	unavailable	https://console.vast.ai/console/create/	125.60	250.00	2026-07-23 09:30:56+00	338f945d-831f-4bf6-bb5d-77d4de69b5d4
vast-ai	gpu	TESLA V100	32.00	\N	\N	0.076889	unavailable	https://console.vast.ai/console/create/	94.00	300.00	2026-07-23 09:30:56+00	29253d5b-18c1-4158-8817-2d8968291a66
vast-ai	gpu	TESLA V100	32.00	\N	\N	0.151556	unavailable	https://console.vast.ai/console/create/	251.10	300.00	2026-07-23 09:30:56+00	b263987f-7d2f-41c9-bbe5-7e2f6ccfaf8e
vast-ai	gpu	TESLA V100	32.00	\N	\N	0.039556	unavailable	https://console.vast.ai/console/create/	62.80	300.00	2026-07-23 09:30:56+00	e64905b3-ebd1-4643-84e5-c612049077c0
vast-ai	gpu	TESLA V100	32.00	\N	\N	0.020889	unavailable	https://console.vast.ai/console/create/	31.40	300.00	2026-07-23 09:30:56+00	fd4f21cf-3d94-43ea-8f30-54f466c3d1c3
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.458294	available	https://console.vast.ai/console/create/	55.10	250.00	2026-07-23 09:30:56+00	4c558c96-05ee-4586-9e0f-7d8280c5d167
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.316296	available	https://console.vast.ai/console/create/	63.00	250.00	2026-07-23 09:30:56+00	18ee2e94-be4a-4c2f-853b-0bf84afe6543
vast-ai	gpu	RTX PRO 6000 S	95.59	\N	\N	1.002963	unavailable	https://console.vast.ai/console/create/	123.40	250.00	2026-07-23 09:30:56+00	15511246-a864-40b5-bb3d-ba4edd8b9bc8
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.281481	available	https://console.vast.ai/console/create/	63.00	250.00	2026-07-23 09:30:56+00	d895e4e3-1a35-413d-a9b8-b5b8b6a57ac1
vast-ai	gpu	H100 NVL	93.58	\N	\N	1.334815	unavailable	https://console.vast.ai/console/create/	314.70	700.00	2026-07-23 09:30:56+00	7607d3d6-0c70-434f-927c-af41fa9f9e9a
vast-ai	gpu	RTX PRO 6000 WS	95.59	\N	\N	1.005185	unavailable	https://console.vast.ai/console/create/	251.90	250.00	2026-07-23 09:30:56+00	c9f19821-57a9-49c2-b385-1bd9741945f8
vast-ai	gpu	RTX PRO 6000 WS	95.59	\N	\N	2.135556	unavailable	https://console.vast.ai/console/create/	188.80	250.00	2026-07-23 09:30:56+00	8b05aea9-7944-4c17-b948-bfec0861e572
vast-ai	gpu	RTX 4090	23.99	\N	\N	0.268889	available	https://console.vast.ai/console/create/	62.90	450.00	2026-07-23 09:30:56+00	9a80a63e-60ed-42c1-8c58-918c022bada8
vast-ai	gpu	RTX 4070S TI	15.99	\N	\N	0.082222	unavailable	https://console.vast.ai/console/create/	62.60	250.00	2026-07-23 09:30:56+00	c8d6c773-35e9-4cc4-a68a-6899aa439114
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.748889	unavailable	https://console.vast.ai/console/create/	125.60	250.00	2026-07-23 09:30:56+00	6fbdc5d1-8b7e-4400-a0fc-d5046becdbbf
vast-ai	gpu	RTX 4080S	15.99	\N	\N	0.093630	unavailable	https://console.vast.ai/console/create/	62.60	320.00	2026-07-23 09:30:56+00	3731598e-411d-48a2-9c0c-59e2db9c6fb3
vast-ai	gpu	RTX PRO 6000 WS	95.59	\N	\N	0.842222	available	https://console.vast.ai/console/create/	172.90	250.00	2026-07-23 09:30:56+00	e8a4f543-7910-49af-88e7-da7bae866e1e
vast-ai	gpu	RTX 5070 TI	15.92	\N	\N	0.095556	unavailable	https://console.vast.ai/console/create/	31.20	250.00	2026-07-23 09:30:56+00	91645ed0-68aa-4583-b129-26ffa549d366
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.403704	unavailable	https://console.vast.ai/console/create/	30.50	250.00	2026-07-23 09:30:56+00	63bab80d-3ef2-42f2-9def-23b425b39d40
vast-ai	gpu	RTX 4090	23.99	\N	\N	0.135556	available	https://console.vast.ai/console/create/	31.40	450.00	2026-07-23 09:30:56+00	1c76a880-4500-4ad9-88d9-55c2a93696c5
vast-ai	gpu	RTX 5090	31.84	\N	\N	1.337037	unavailable	https://console.vast.ai/console/create/	212.40	250.00	2026-07-23 09:30:56+00	69e1cc01-7856-4311-bd95-c84d25a4cbe0
vast-ai	gpu	RTX 4080S	15.99	\N	\N	0.098222	unavailable	https://console.vast.ai/console/create/	62.60	320.00	2026-07-23 09:30:56+00	16a3e4ad-5eda-4755-8dc9-29d72d4b73b4
vast-ai	gpu	RTX 5070	11.94	\N	\N	0.431111	unavailable	https://console.vast.ai/console/create/	125.80	250.00	2026-07-23 09:30:56+00	9f27eb95-26b9-4eb7-8322-1fd8a7ad6fc8
vast-ai	gpu	RTX 5070 TI	15.92	\N	\N	0.270370	unavailable	https://console.vast.ai/console/create/	62.90	250.00	2026-07-23 09:30:56+00	08bb1b27-a4ed-4ab1-9a70-a9980aafc4a8
vast-ai	gpu	RTX 4090	47.99	\N	\N	0.297037	unavailable	https://console.vast.ai/console/create/	62.90	450.00	2026-07-23 09:30:56+00	25457bd7-2d3b-41f1-932c-986a1a7ef891
vast-ai	gpu	RTX 3090	24.00	\N	\N	0.069630	unavailable	https://console.vast.ai/console/create/	62.70	350.00	2026-07-23 09:30:56+00	c61bf1b4-7c3c-4c35-b5cf-abf0af82178a
vast-ai	gpu	H100 SXM	79.65	\N	\N	2.935556	unavailable	https://console.vast.ai/console/create/	431.90	700.00	2026-07-23 09:30:56+00	ad56a00d-77ce-401b-bf23-1ea3bd37d83e
vast-ai	gpu	RTX 5080	15.92	\N	\N	0.155111	unavailable	https://console.vast.ai/console/create/	30.50	250.00	2026-07-23 09:30:56+00	21794b1a-fb7f-40f8-822d-4f51c0f806ff
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.915107	available	https://console.vast.ai/console/create/	110.20	250.00	2026-07-23 09:30:56+00	15cde916-3964-4684-a452-03f60d9b5a67
vast-ai	gpu	RTX PRO 4500	31.86	\N	\N	0.335556	unavailable	https://console.vast.ai/console/create/	188.60	250.00	2026-07-23 09:30:56+00	d3a603c5-bc86-48db-b0d6-88565305b303
vast-ai	gpu	RTX 5070	11.94	\N	\N	0.244444	unavailable	https://console.vast.ai/console/create/	83.50	250.00	2026-07-23 09:30:56+00	559b32d8-613e-4f88-90cf-40fa69caa67a
vast-ai	gpu	RTX PRO 6000 S	95.59	\N	\N	2.669630	unavailable	https://console.vast.ai/console/create/	377.80	250.00	2026-07-23 09:30:56+00	47654bd7-62db-47fd-bb41-7b856fd031f7
vast-ai	gpu	RTX 4090	23.99	\N	\N	0.535556	unavailable	https://console.vast.ai/console/create/	125.70	450.00	2026-07-23 09:30:56+00	adeb94a4-ce6b-42c7-9e43-0d2a0b74debc
vast-ai	gpu	RTX 5070	11.94	\N	\N	0.857778	unavailable	https://console.vast.ai/console/create/	251.50	250.00	2026-07-23 09:30:56+00	f8b91362-fe0a-4a85-86ce-2913fde4f249
vast-ai	gpu	RTX 4090	47.99	\N	\N	0.935556	unavailable	https://console.vast.ai/console/create/	251.40	450.00	2026-07-23 09:30:56+00	55d1c305-b068-4c72-9831-c14824d18eb5
vast-ai	gpu	RTX PRO 5000	47.79	\N	\N	1.282222	unavailable	https://console.vast.ai/console/create/	125.80	250.00	2026-07-23 09:30:56+00	8658f760-4c3d-4110-9916-9a43512bc411
vast-ai	gpu	RTX PRO 6000 WS	95.59	\N	\N	1.329037	unavailable	https://console.vast.ai/console/create/	125.90	250.00	2026-07-23 09:30:56+00	4fb89425-77a6-4a20-ae4c-d09796cd3ae8
vast-ai	gpu	RTX 4090	47.99	\N	\N	0.590370	unavailable	https://console.vast.ai/console/create/	125.90	450.00	2026-07-23 09:30:56+00	5a3dbc62-ed9d-410d-aae6-221190d7e648
vast-ai	gpu	RTX 3080 TI	12.00	\N	\N	0.103556	unavailable	https://console.vast.ai/console/create/	20.40	320.00	2026-07-23 09:30:56+00	6e49d45e-c3de-407b-86bb-e0a925e90e72
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.470370	available	https://console.vast.ai/console/create/	30.50	250.00	2026-07-23 09:30:56+00	e1576d62-f700-4c5f-bb4e-5d7eabe358dd
vast-ai	gpu	H100 NVL	93.58	\N	\N	1.334815	unavailable	https://console.vast.ai/console/create/	125.40	700.00	2026-07-23 09:30:56+00	45dd9766-ad0d-4cc2-b527-781fb0b5a924
vast-ai	gpu	RTX 5080	15.92	\N	\N	0.116889	unavailable	https://console.vast.ai/console/create/	55.00	250.00	2026-07-23 09:30:56+00	3b85aee0-7efe-45b4-a737-d3658405533d
vast-ai	gpu	L4	22.49	\N	\N	0.026963	unavailable	https://console.vast.ai/console/create/	21.30	250.00	2026-07-23 09:30:56+00	cfa03cb6-aaad-4bd4-b05a-e6e9aae99227
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.212889	unavailable	https://console.vast.ai/console/create/	62.60	250.00	2026-07-23 09:30:56+00	603988d5-79d8-4310-8da9-ef14d89c3a90
vast-ai	gpu	RTX 5060 TI	15.93	\N	\N	0.070370	unavailable	https://console.vast.ai/console/create/	31.40	250.00	2026-07-23 09:30:56+00	7bb0b15c-ebb7-483f-b2e1-e19323d680df
vast-ai	gpu	RTX 5090	31.84	\N	\N	1.337037	unavailable	https://console.vast.ai/console/create/	188.80	250.00	2026-07-23 09:30:56+00	f14c93e1-3026-4a2a-a649-5f05c65f1fb1
vast-ai	gpu	RTX PRO 6000 S	95.59	\N	\N	3.469630	unavailable	https://console.vast.ai/console/create/	251.90	250.00	2026-07-23 09:30:56+00	c9fa1638-cf29-45f4-bd92-fb8d9bf80541
vast-ai	gpu	RTX 4090	23.99	\N	\N	0.321407	unavailable	https://console.vast.ai/console/create/	125.60	450.00	2026-07-23 09:30:56+00	19f4e20d-443f-4bfe-bcc9-93f16cc9951b
vast-ai	gpu	L40S	44.99	\N	\N	0.428593	unavailable	https://console.vast.ai/console/create/	118.10	350.00	2026-07-23 09:30:56+00	0e2df066-c9e2-4909-87c5-17bae0e7dd95
vast-ai	gpu	RTX 4090	47.99	\N	\N	0.468889	unavailable	https://console.vast.ai/console/create/	125.70	450.00	2026-07-23 09:30:56+00	d2ca128d-2151-46b5-8795-b73c50d1cff5
vast-ai	gpu	RTX 6000ADA	47.99	\N	\N	0.698222	unavailable	https://console.vast.ai/console/create/	167.90	250.00	2026-07-23 09:30:56+00	f3389736-a26f-4af7-b702-3ecf3b752de2
vast-ai	gpu	RTX 4090	23.99	\N	\N	0.188889	available	https://console.vast.ai/console/create/	61.90	450.00	2026-07-23 09:30:56+00	cb320a66-0856-451e-bc17-7ac7e0606649
vast-ai	gpu	RTX 5070	11.94	\N	\N	0.090370	unavailable	https://console.vast.ai/console/create/	31.40	250.00	2026-07-23 09:30:56+00	828c8406-6d1b-49a6-99d9-0940690d0ab5
vast-ai	gpu	RTX PRO 6000 S	95.59	\N	\N	1.736296	unavailable	https://console.vast.ai/console/create/	125.90	250.00	2026-07-23 09:30:56+00	c4ee257a-dcf0-4334-aee2-a85c69717782
vast-ai	gpu	RTX 5070 TI	15.92	\N	\N	0.268889	available	https://console.vast.ai/console/create/	62.60	250.00	2026-07-23 09:30:56+00	2ee6e787-1ea2-42a1-b4a1-796e5d1da4cf
vast-ai	gpu	RTX 6000ADA	47.99	\N	\N	0.350222	unavailable	https://console.vast.ai/console/create/	83.90	250.00	2026-07-23 09:30:56+00	e200114e-8981-4a05-9ef4-e8a2a839aa5b
vast-ai	gpu	RTX 3080 TI	12.00	\N	\N	0.052889	unavailable	https://console.vast.ai/console/create/	10.20	320.00	2026-07-23 09:30:56+00	45631394-d3ea-425b-87c6-80336a5e07ca
vast-ai	gpu	RTX PRO 4500	31.86	\N	\N	0.215556	unavailable	https://console.vast.ai/console/create/	503.80	250.00	2026-07-23 09:30:56+00	c45e92f6-0989-41a6-b6f4-df7a88f07aad
vast-ai	gpu	RTX 5080	15.92	\N	\N	0.376296	unavailable	https://console.vast.ai/console/create/	100.70	250.00	2026-07-23 09:30:56+00	b4673967-5b8a-42b2-906d-f88d8ce42d73
vast-ai	gpu	RTX 5090	31.84	\N	\N	0.934815	available	https://console.vast.ai/console/create/	125.70	250.00	2026-07-23 09:30:56+00	52d2aa1c-6801-4633-8817-b8ca88ba4cad
vast-ai	gpu	RTX 5070 TI	15.92	\N	\N	0.537037	unavailable	https://console.vast.ai/console/create/	125.70	250.00	2026-07-23 09:30:56+00	938f4dd1-4327-41b8-bc74-3c1de8b62805
vast-ai	gpu	RTX PRO 5000	47.79	\N	\N	0.668148	unavailable	https://console.vast.ai/console/create/	63.00	250.00	2026-07-23 09:30:56+00	5a34795a-58cb-42d4-9289-037b723c5de7
vast-ai	gpu	RTX 4090D	23.99	\N	\N	0.388148	unavailable	https://console.vast.ai/console/create/	125.90	450.00	2026-07-23 09:30:56+00	33bd6775-3af1-458b-83e6-42f83b5da6c5
vessl	gpu	H100 SXM	80.00	\N	\N	2.390000	available	https://vessl.ai/ko/pricing	256.00	700.00	2026-07-22 18:01:11+00	a10dee99-22c1-4a21-981f-2ed9f0ee67c4
vessl	gpu	A100 SXM	80.00	\N	\N	1.550000	available	https://vessl.ai/ko/pricing	128.00	400.00	2026-07-22 18:01:11+00	5be4c55a-62c4-4478-b1fc-68d4ca973835
vessl	gpu	A100 PCIE	40.00	\N	\N	1.100000	available	https://vessl.ai/ko/pricing	128.00	400.00	2026-07-22 18:01:11+00	f8f0f76a-1eb8-4356-8bb2-9d3d385b4740
vessl	gpu	RTX 4090	24.00	\N	\N	0.890000	available	https://vessl.ai/ko/pricing	64.00	450.00	2026-07-22 18:01:11+00	ac08e312-6b5e-4875-ac5f-827aee8784ca
vessl	gpu	H100 SXM	80.00	\N	\N	2.390000	available	https://vessl.ai/ko/pricing	256.00	700.00	2026-07-22 19:09:22+00	b453bab3-d3d6-4891-8d32-d1a78c2f58ee
vessl	gpu	A100 SXM	80.00	\N	\N	1.550000	available	https://vessl.ai/ko/pricing	128.00	400.00	2026-07-22 19:09:22+00	f51bdeff-5c5b-455e-8abf-68fa6e30a3f5
vessl	gpu	A100 PCIE	40.00	\N	\N	1.100000	available	https://vessl.ai/ko/pricing	128.00	400.00	2026-07-22 19:09:22+00	51ac6cdf-24d2-4f8f-a736-e4dcbf4ac760
vessl	gpu	RTX 4090	24.00	\N	\N	0.890000	available	https://vessl.ai/ko/pricing	64.00	450.00	2026-07-22 19:09:22+00	f686bed3-13cb-49c3-ba4b-0dea6e7d836f
vessl	gpu	H100 SXM	80.00	\N	\N	2.390000	available	https://vessl.ai/ko/pricing	256.00	700.00	2026-07-22 19:19:16+00	3a725a7f-4aed-42ab-b279-90c206456a83
vessl	gpu	A100 SXM	80.00	\N	\N	1.550000	available	https://vessl.ai/ko/pricing	128.00	400.00	2026-07-22 19:19:16+00	117a5159-c90c-4ea4-99a1-916c83860fc5
vessl	gpu	A100 PCIE	40.00	\N	\N	1.100000	available	https://vessl.ai/ko/pricing	128.00	400.00	2026-07-22 19:19:16+00	85e69f0e-baa1-4457-b456-e1bc5833c473
vessl	gpu	RTX 4090	24.00	\N	\N	0.890000	available	https://vessl.ai/ko/pricing	64.00	450.00	2026-07-22 19:19:16+00	8a362a30-60f6-4686-b5d4-1c0d26808513
vessl	gpu	H100 SXM	80.00	\N	\N	2.390000	available	https://vessl.ai/ko/pricing	256.00	700.00	2026-07-23 09:23:14+00	944f988a-c076-4314-a3a5-f062a72d7a04
vessl	gpu	A100 SXM	80.00	\N	\N	1.550000	available	https://vessl.ai/ko/pricing	128.00	400.00	2026-07-23 09:23:14+00	a55de882-24e2-423d-8529-ffb3636713c0
vessl	gpu	A100 PCIE	40.00	\N	\N	1.100000	available	https://vessl.ai/ko/pricing	128.00	400.00	2026-07-23 09:23:14+00	78ff340b-d1fb-4114-a11c-7ee71ca9fd62
vessl	gpu	RTX 4090	24.00	\N	\N	0.890000	available	https://vessl.ai/ko/pricing	64.00	450.00	2026-07-23 09:23:14+00	dc51711e-2fd8-4a7c-ba49-8643e7f26b81
vessl	gpu	H100 SXM	80.00	\N	\N	2.390000	available	https://vessl.ai/ko/pricing	256.00	700.00	2026-07-23 09:31:13+00	71665708-b2f0-4656-8237-4304d7cc87a5
vessl	gpu	A100 SXM	80.00	\N	\N	1.550000	available	https://vessl.ai/ko/pricing	128.00	400.00	2026-07-23 09:31:13+00	fac913fa-1b57-408b-a824-e4e389e0a57d
vessl	gpu	A100 PCIE	40.00	\N	\N	1.100000	available	https://vessl.ai/ko/pricing	128.00	400.00	2026-07-23 09:31:13+00	6207f0ac-3168-43fe-a92a-df1f4bead426
vessl	gpu	RTX 4090	24.00	\N	\N	0.890000	available	https://vessl.ai/ko/pricing	64.00	450.00	2026-07-23 09:31:13+00	05578770-27e5-4118-b9c7-0ced312439f0
runpod	gpu	MI300X	192.00	\N	\N	2.390000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	751bbdba-272a-4ecd-bee1-34987517b9b7
runpod	gpu	A100 PCIE	80.00	\N	\N	1.390000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	e5d9f65b-97dc-43db-8a22-d7fd1e1cd633
runpod	gpu	A100 SXM 40GB	40.00	\N	\N	1.000000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	34bd11fe-ff76-41c8-9f2f-3a18da2aeb5e
runpod	gpu	A100 SXM	80.00	\N	\N	1.490000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	f8cfef53-5267-4269-a61c-f7c4cb0c7f0d
runpod	gpu	A40	48.00	\N	\N	0.440000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	bd5ac1a2-8363-4f3f-9c08-e981b7fff6ed
runpod	gpu	B200	180.00	\N	\N	5.890000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	9df9e30d-ad4b-4dbd-9625-efd0d96027c3
runpod	gpu	B300	288.00	\N	\N	7.390000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	19c621b6-3939-42e7-b331-2b0a70d24354
runpod	gpu	NVIDIA GEFORCE GTX 1050 TI	4.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	60cd33fe-d765-46c9-a2f0-dced97c1fe72
runpod	gpu	RTX 3070	8.00	\N	\N	0.130000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	5b37deb4-072a-44fd-ae47-60907b4a6457
runpod	gpu	RTX 3080	10.00	\N	\N	0.170000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	5903ced2-b95b-4caf-80e1-925cc29596f0
runpod	gpu	RTX 3080 TI	12.00	\N	\N	0.180000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	3ecd7d6d-9522-4125-8318-1c0309e2aa29
runpod	gpu	RTX 3090	24.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	e462531a-a673-433f-b624-388f3cd69b2e
runpod	gpu	RTX 3090 TI	24.00	\N	\N	0.460000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	ce627a7d-a242-42e8-930e-aff1ae96d5ff
runpod	gpu	RTX 4070 TI	12.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	76770ceb-7bfb-4fd9-8a09-f15f8bd98c61
runpod	gpu	RTX 4080	16.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	73454370-7e91-46f6-bd4d-909484dcf726
runpod	gpu	RTX 4080 SUPER	16.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	e5abba61-3be2-4012-a6fc-76c3dabeeb69
runpod	gpu	RTX 4090	24.00	\N	\N	0.690000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	4404d419-d5da-42e4-b90f-14e8b1653c69
runpod	gpu	RTX 5080	16.00	\N	\N	0.590000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	5f2f1f6b-b3c3-4025-98e5-5a8ec25605ae
runpod	gpu	RTX 5090	32.00	\N	\N	0.990000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	bf7d726e-3a91-43e5-806c-02c705dd0110
runpod	gpu	H100 SXM	80.00	\N	\N	2.990000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	e49074d8-0884-4b84-99fb-ce1f6c5057c5
runpod	gpu	H100 NVL	94.00	\N	\N	3.190000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	5c1ca999-4c6c-40b6-90f2-4cfcd9086cae
runpod	gpu	H100 PCIE	80.00	\N	\N	2.890000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	0cb74e5d-527a-4ab3-992a-27b6a7cfff7f
runpod	gpu	H200 SXM	141.00	\N	\N	4.390000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	b2db3035-acce-4d60-a16f-f529ef561288
runpod	gpu	H200 NVL	143.00	\N	\N	3.790000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	055bce63-8b13-43db-ab31-1ef24d12fb59
runpod	gpu	L4	24.00	\N	\N	0.390000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	5781bb4a-7240-4c03-92f1-382a73c49934
runpod	gpu	L40	48.00	\N	\N	0.820000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	68980feb-acfc-444d-bedf-8849b41adf2b
runpod	gpu	L40S	48.00	\N	\N	0.990000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	035acb6d-2d82-4b67-b032-44a938146a7c
runpod	gpu	RTX 2000 ADA	16.00	\N	\N	0.240000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	dfc810e2-0695-4c61-9c11-f6770d63fa25
runpod	gpu	RTX 4000 ADA	20.00	\N	\N	0.280000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	48cf6c16-92fe-4f01-a755-9f68b1cd7c39
runpod	gpu	RTX 4000 ADA SFF	20.00	\N	\N	0.440000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	925b0872-ef1b-471e-bea5-90ea56a44d99
runpod	gpu	RTX 5000 ADA	32.00	\N	\N	0.830000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	8ba2d1d6-e155-40b3-8ccf-96586630ea2d
runpod	gpu	RTX 6000 ADA	48.00	\N	\N	0.840000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	60ba2132-b848-4f45-9745-8e28f3e25b2c
runpod	gpu	RTX A2000	6.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	e2b1e543-7152-49b8-b79b-e1ebd9690baf
runpod	gpu	RTX A4000	16.00	\N	\N	0.250000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	4196542d-34cc-4c5d-acd9-6279806035f6
runpod	gpu	RTX A4500	20.00	\N	\N	0.250000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	8907bbde-3e3d-4a4e-a71e-517db5f9a735
runpod	gpu	RTX A5000	24.00	\N	\N	0.270000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	9c443f95-21a2-42ad-beb5-6ddfb6a76662
runpod	gpu	RTX A6000	48.00	\N	\N	0.530000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	02b974f3-b50f-4a23-80e0-fc2838ae558a
runpod	gpu	RTX PRO 4000	24.00	\N	\N	0.570000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	7322327f-5e48-474f-b372-e5b34c2e4b6a
runpod	gpu	RTX PRO 4500	32.00	\N	\N	0.740000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	dc574974-9992-4171-9a0f-348ded5a2b29
runpod	gpu	RTX PRO 5000	48.00	\N	\N	0.960000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	dae37ee7-f721-41f8-b632-63b08649b2cf
runpod	gpu	RTX PRO 6000 MAXQ	96.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	58f580ce-884a-4734-83ba-87f513a16591
runpod	gpu	RTX PRO 6000	96.00	\N	\N	1.990000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	d1deeffc-d5a7-47aa-9bc2-10c44a88413e
runpod	gpu	PRO 6000 MIG 24GB	24.00	\N	\N	0.490000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	0cb5eabe-54f2-45a5-a941-2ab8b25d228d
runpod	gpu	PRO 6000 MIG 48GB	48.00	\N	\N	1.000000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	d1662ea4-f47f-41d5-868d-63fe2dd467f7
runpod	gpu	RTX PRO 6000 WK	96.00	\N	\N	1.890000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	322329a2-e037-4c88-a89c-ea4fc16731fe
runpod	gpu	TESLA V100	16.00	\N	\N	0.190000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	7bbbbb47-4233-40f4-94bf-3be008aa8320
runpod	gpu	V100 SXM2	16.00	\N	\N	0.230000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	50c3e910-ef1a-48e4-8179-6d78b54d9a95
aws	gpu	UNKNOWN GPU	0.00	\N	\N	2.288000	available	https://aws.amazon.com/ec2/instance-types/g6e/	\N	\N	2026-07-23 10:29:26+00	0ca7bef8-5f01-406e-93f8-cb43f2cd1ced
aws	gpu	UNKNOWN GPU	0.00	\N	\N	18.522300	available	https://aws.amazon.com/ec2/instance-types/g6e/	\N	\N	2026-07-23 10:29:26+00	ca04f53c-56c0-4b0c-ab4e-5b9e7e71de83
aws	gpu	L4	0.00	\N	\N	23.658200	available	https://aws.amazon.com/ec2/instance-types/g6/	\N	\N	2026-07-23 10:29:26+00	b5ea521a-67c7-4592-8ada-d5ab045349f7
aws	gpu	T4	0.00	\N	\N	0.925000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	\N	\N	2026-07-23 10:29:26+00	994cfab9-4c33-4d09-b53e-96ae0f19da1b
aws	gpu	L4	0.00	\N	\N	44.208000	available	https://aws.amazon.com/ec2/instance-types/g6/	\N	\N	2026-07-23 10:29:26+00	6ab709f2-00c9-4cdc-b940-ae1cbc1dc05a
aws	gpu	UNKNOWN GPU	0.00	\N	\N	0.719300	available	https://aws.amazon.com/ec2/instance-types/g6f/	\N	\N	2026-07-23 10:29:26+00	7d99ec93-9bc6-48de-97d9-15aac7883984
aws	gpu	A10G	0.00	\N	\N	1.996900	available	https://aws.amazon.com/ec2/instance-types/g5/	\N	\N	2026-07-23 10:29:26+00	937b230a-34d2-4683-ba88-322e1d10387c
aws	gpu	V100	0.00	\N	\N	33.872000	available	https://aws.amazon.com/ec2/instance-types/p3/	\N	\N	2026-07-23 10:29:26+00	09296029-4d99-4436-9d52-c9c68de5800a
aws	gpu	L4	0.00	\N	\N	2.162100	available	https://aws.amazon.com/ec2/instance-types/g6/	\N	\N	2026-07-23 10:29:26+00	21397e7e-ba87-4b88-9f9a-8ec1221995c9
aws	gpu	UNKNOWN GPU	0.00	\N	\N	2.756500	available	https://aws.amazon.com/ec2/instance-types/g6e/	\N	\N	2026-07-23 10:29:26+00	0932645b-0c36-4e10-84a9-e74276287ff4
aws	gpu	L4	0.00	\N	\N	1.469600	available	https://aws.amazon.com/ec2/instance-types/g6/	\N	\N	2026-07-23 10:29:26+00	4b2e4019-44d9-4b72-8a30-b5530e93b946
aws	gpu	UNKNOWN GPU	0.00	\N	\N	0.292000	available	https://aws.amazon.com/ec2/instance-types/g6f/	\N	\N	2026-07-23 10:29:26+00	8cc4f3c8-c414-4b24-82b0-6219de2b09c9
aws	gpu	L4	0.00	\N	\N	3.017700	available	https://aws.amazon.com/ec2/instance-types/g6/	\N	\N	2026-07-23 10:29:26+00	dcf1a832-b99f-4392-b942-0499d77f31a4
aws	gpu	UNKNOWN GPU	0.00	\N	\N	0.248400	available	https://aws.amazon.com/ec2/instance-types/g6f/	\N	\N	2026-07-23 10:29:26+00	96bf30e7-2986-424c-8c28-fdec936357c6
aws	gpu	A10G	0.00	\N	\N	3.010100	available	https://aws.amazon.com/ec2/instance-types/g5/	\N	\N	2026-07-23 10:29:26+00	372f8044-724c-497c-87ec-82cc8b00d851
aws	gpu	UNKNOWN GPU	0.00	\N	\N	1.018500	available	https://aws.amazon.com/ec2/instance-types/g5g/	\N	\N	2026-07-23 10:29:26+00	81078e75-3b0b-4f54-a59d-180decb58876
aws	gpu	L4	0.00	\N	\N	5.258400	available	https://aws.amazon.com/ec2/instance-types/g6/	\N	\N	2026-07-23 10:29:26+00	651e0098-d307-449b-8d40-8675adfc9c46
aws	gpu	V100	0.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	\N	\N	2026-07-23 10:29:26+00	d64b12a8-cba1-414a-87d3-6a47f82eb431
aws	gpu	T4	0.00	\N	\N	1.481000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	\N	\N	2026-07-23 10:29:26+00	def2d88a-f76d-45ce-9dfb-98991e660945
aws	gpu	UNKNOWN GPU	0.00	\N	\N	0.683900	available	https://aws.amazon.com/ec2/instance-types/g5g/	\N	\N	2026-07-23 10:29:26+00	069c4abc-dd57-4b44-85a5-e6ad37b67898
aws	gpu	UNKNOWN GPU	0.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	\N	\N	2026-07-23 10:29:26+00	38646492-c357-44ae-a2b4-d6e3e1235003
aws	gpu	UNKNOWN GPU	0.00	\N	\N	3.375200	available	https://aws.amazon.com/ec2/instance-types/g5g/	\N	\N	2026-07-23 10:29:26+00	b1f22d5c-7394-4ce0-a4f9-f4ca9b6d185e
aws	gpu	T4	0.00	\N	\N	0.647000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	\N	\N	2026-07-23 10:29:26+00	e4f44b28-1013-4945-a031-5c6985b6af93
aws	gpu	T4	0.00	\N	\N	4.812000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	\N	\N	2026-07-23 10:29:26+00	06dffade-4e79-4a49-bd60-78e3eb7685fd
aws	gpu	T4	0.00	\N	\N	5.353000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	\N	\N	2026-07-23 10:29:26+00	7a35f46b-0d15-4372-a8b9-fb8358c6c909
aws	gpu	T4	0.00	\N	\N	9.624000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	\N	\N	2026-07-23 10:29:26+00	27aa2a1f-03df-4e9c-9917-fc3423134051
aws	gpu	A10G	0.00	\N	\N	6.974400	available	https://aws.amazon.com/ec2/instance-types/g5/	\N	\N	2026-07-23 10:29:26+00	b9ccd741-f780-490a-a665-b3e538f9aee3
aws	gpu	UNKNOWN GPU	0.00	\N	\N	7.168100	available	https://aws.amazon.com/ec2/instance-types/g6f/	\N	\N	2026-07-23 10:29:26+00	2d9f1213-87d1-4937-a6fd-762229791f14
aws	gpu	A10G	0.00	\N	\N	10.014000	available	https://aws.amazon.com/ec2/instance-types/g5/	\N	\N	2026-07-23 10:29:26+00	2fc99c6d-b289-49ca-be11-6afefaab2115
aws	gpu	V100	0.00	\N	\N	16.936000	available	https://aws.amazon.com/ec2/instance-types/p3/	\N	\N	2026-07-23 10:29:26+00	488d7831-7358-491c-a760-d869b47c94eb
aws	gpu	L4	0.00	\N	\N	19.660800	available	https://aws.amazon.com/ec2/instance-types/g6/	\N	\N	2026-07-23 10:29:26+00	3ed60298-09ea-4ccf-9492-2bf46584654e
aws	gpu	T4	0.00	\N	\N	2.677000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	\N	\N	2026-07-23 10:29:26+00	2d31412c-7cd0-486d-861f-d42126c2835a
aws	gpu	UNKNOWN GPU	0.00	\N	\N	87.348500	available	https://aws.amazon.com/ec2/instance-types/p5en/	\N	\N	2026-07-23 10:29:26+00	88e9c9d8-3733-4ffd-9b4d-e255a32e73ec
aws	gpu	A10G	0.00	\N	\N	5.036500	available	https://aws.amazon.com/ec2/instance-types/g5/	\N	\N	2026-07-23 10:29:26+00	ce6787bc-24e8-49ad-b7f5-639f66f33e19
aws	gpu	UNKNOWN GPU	0.00	\N	\N	12.900100	available	https://aws.amazon.com/ec2/instance-types/g6e/	\N	\N	2026-07-23 10:29:26+00	aae3442d-307a-483e-95aa-16864f547413
aws	gpu	L4	0.00	\N	\N	7.627000	available	https://aws.amazon.com/ec2/instance-types/g6/	\N	\N	2026-07-23 10:29:26+00	52e77647-c950-4bf5-bed0-25efae332f44
aws	gpu	H100	0.00	\N	\N	75.955200	available	https://aws.amazon.com/ec2/instance-types/p5/	\N	\N	2026-07-23 10:29:26+00	b3a57bfb-066f-4102-b876-6ac7c55ec7d1
aws	gpu	UNKNOWN GPU	0.00	\N	\N	3.375200	available	https://aws.amazon.com/ec2/instance-types/g5g/	\N	\N	2026-07-23 10:29:26+00	5099b71e-ed99-4bdb-a721-52e1e84c5aca
aws	gpu	A100	0.00	\N	\N	30.410300	available	https://aws.amazon.com/ec2/instance-types/p4d/	\N	\N	2026-07-23 10:29:26+00	ad7c947d-a8b9-4dd6-8046-a19cfe28613f
aws	gpu	UNKNOWN GPU	0.00	\N	\N	0.516600	available	https://aws.amazon.com/ec2/instance-types/g5g/	\N	\N	2026-07-23 10:29:26+00	6f320c09-09be-4cca-ae0b-46ec195a7d4a
aws	gpu	A10G	0.00	\N	\N	1.490300	available	https://aws.amazon.com/ec2/instance-types/g5/	\N	\N	2026-07-23 10:29:26+00	2d3d0c3b-d48d-447e-9f4d-e959ae197a60
aws	gpu	UNKNOWN GPU	0.00	\N	\N	37.044700	available	https://aws.amazon.com/ec2/instance-types/g6e/	\N	\N	2026-07-23 10:29:26+00	3869ed60-0f05-4870-a59d-b04b563b02d7
aws	gpu	A10G	0.00	\N	\N	1.237000	available	https://aws.amazon.com/ec2/instance-types/g5/	\N	\N	2026-07-23 10:29:26+00	be1689bf-b078-46a3-b7d8-36a08782e498
aws	gpu	UNKNOWN GPU	0.00	\N	\N	3.693600	available	https://aws.amazon.com/ec2/instance-types/g6e/	\N	\N	2026-07-23 10:29:26+00	064d5d8a-5732-49b9-8783-753f56e7ed5d
aws	gpu	UNKNOWN GPU	0.00	\N	\N	5.567600	available	https://aws.amazon.com/ec2/instance-types/g6e/	\N	\N	2026-07-23 10:29:26+00	52e546b7-011e-4a13-b600-fd699b444475
aws	gpu	A10G	0.00	\N	\N	20.028100	available	https://aws.amazon.com/ec2/instance-types/g5/	\N	\N	2026-07-23 10:29:26+00	dc31404d-4982-47b5-9950-83b4099d5c5b
aws	gpu	INFERENTIA2	0.00	\N	\N	0.909800	available	https://aws.amazon.com/ec2/instance-types/inf2/	\N	\N	2026-07-23 10:29:26+00	bc1006bb-236c-479c-8fe7-02f18a353151
aws	gpu	UNKNOWN GPU	0.00	\N	\N	9.315700	available	https://aws.amazon.com/ec2/instance-types/g6e/	\N	\N	2026-07-23 10:29:26+00	2a3149dc-8b07-4e72-9d0c-abea735b3d48
vessl	gpu	B300	288.00	\N	\N	7.290000	available	https://vessl.ai/ko/pricing	\N	\N	2026-07-23 10:29:26+00	b1688f01-36bf-49c6-b5c4-5eb89d38cc46
vessl	gpu	B200	192.00	\N	\N	5.790000	available	https://vessl.ai/ko/pricing	\N	\N	2026-07-23 10:29:26+00	25e1d31b-5361-469f-a981-e3cb0e95f0e4
vessl	gpu	H200 SXM	141.00	\N	\N	4.290000	available	https://vessl.ai/ko/pricing	\N	\N	2026-07-23 10:29:26+00	8d407286-8bb3-4e22-8291-e69ce9a87db0
vessl	gpu	H100 SXM	80.00	\N	\N	3.190000	available	https://vessl.ai/ko/pricing	\N	\N	2026-07-23 10:29:26+00	7c3c35ba-7f6c-4edf-b31d-c65f7975b856
vessl	gpu	A100 SXM	80.00	\N	\N	1.390000	available	https://vessl.ai/ko/pricing	\N	\N	2026-07-23 10:29:26+00	81020c64-db5e-49c1-80d4-86462c29ba65
vessl	gpu	L40S	48.00	\N	\N	1.800000	available	https://vessl.ai/ko/pricing	\N	\N	2026-07-23 10:29:26+00	641e7468-51bf-43a0-aa59-aea4825a33f0
gpuaas	gpu	H100 SXM	80.00	\N	\N	2.390000	available	https://gpuaas.kr/	\N	\N	2026-07-23 10:29:26+00	4c133724-c2c0-43c7-9fba-74ede7a86cf1
gpuaas	gpu	H100 SXM (연간계약)	80.00	\N	\N	2.200000	available	https://gpuaas.kr/	\N	\N	2026-07-23 10:29:26+00	b6bcddf9-274e-480f-92a7-5b05c7415de8
cloudv	gpu	A100 40GB	40.00	\N	\N	0.188400	available	https://cloudv.kr/server/gpu.html	\N	\N	2026-07-23 10:29:26+00	792d2f93-7b6d-4480-a66d-e6807266a20a
cloudv	gpu	A100 40GB	40.00	\N	\N	0.312500	available	https://cloudv.kr/server/gpu.html	\N	\N	2026-07-23 10:29:26+00	ef0ef08e-e0b1-470b-9c97-2c774a388666
cloudv	gpu	A100 40GB	40.00	\N	\N	0.560700	available	https://cloudv.kr/server/gpu.html	\N	\N	2026-07-23 10:29:26+00	4fad0fdf-e447-40e2-9348-e31f351e742c
cloudv	gpu	A100 80GB	80.00	\N	\N	0.226100	available	https://cloudv.kr/server/gpu.html	\N	\N	2026-07-23 10:29:26+00	736e3014-dfa1-4dcb-8fb0-2881d317bd92
cloudv	gpu	A100 80GB	80.00	\N	\N	0.375000	available	https://cloudv.kr/server/gpu.html	\N	\N	2026-07-23 10:29:26+00	77c07266-25fd-4db0-9827-81b6c9df5687
cloudv	gpu	A100 80GB	80.00	\N	\N	0.672800	available	https://cloudv.kr/server/gpu.html	\N	\N	2026-07-23 10:29:26+00	80c58276-f5b9-404c-b541-efb7b964ee00
cloudv	gpu	PRO 5000	48.00	\N	\N	0.188400	available	https://cloudv.kr/server/gpu.html	\N	\N	2026-07-23 10:29:26+00	79ddec99-5f18-4829-9cf2-6098377b6215
cloudv	gpu	PRO 6000	96.00	\N	\N	0.188400	available	https://cloudv.kr/server/gpu.html	\N	\N	2026-07-23 10:29:26+00	173edc2c-df6f-4049-bbae-ab48de0a26c8
cloudv	gpu	RTX 5060	16.00	\N	\N	0.120900	available	https://cloudv.kr/server/gpu.html	\N	\N	2026-07-23 10:29:26+00	98b18135-be79-49e2-a8a2-5f8f8c25508b
cloudv	gpu	RTX 5090	32.00	\N	\N	0.262400	available	https://cloudv.kr/server/gpu.html	\N	\N	2026-07-23 10:29:26+00	b07b7d5a-eedc-4791-8b1c-92349f6a19bc
runyourai	gpu	H100	80.00	\N	\N	2.619600	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	9101304d-83d1-4837-b272-d710ef91e993
runyourai	gpu	B200	192.00	\N	\N	6.776100	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	0a7d6fa3-46d5-4968-814a-19a82df8ccc4
runyourai	gpu	L40S	48.00	\N	\N	1.232600	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	16640aa2-6b30-488b-91b2-a47cf406af37
runyourai	gpu	RTX	0.00	\N	\N	0.817400	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	124e3984-3103-4802-b2f1-4c81e1fe7b5a
runyourai	gpu	RTX	0.00	\N	\N	0.540600	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	e06e583b-6508-4691-89fc-91c7fac10193
runyourai	gpu	RTX	0.00	\N	\N	0.913800	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	28a1035b-b49b-41a6-89e3-22e179e046ab
runyourai	gpu	A100	80.00	\N	\N	1.925400	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	b609ea34-f778-45e8-ab81-0fd3badc6201
runyourai	gpu	A100	40.00	\N	\N	1.454300	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	9699ee10-2b37-4959-a07a-5a3dd79a4bab
runyourai	gpu	RTX	0.00	\N	\N	0.332600	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	e042983a-9238-478e-bd92-e30533162683
runyourai	gpu	L40S	48.00	\N	\N	1.509400	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	60416ae7-5255-4d43-838a-c85204e293e7
runyourai	gpu	H200	80.00	\N	\N	4.004300	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	7098679f-8b28-41d1-a449-2b7d75087444
runyourai	gpu	H100	80.00	\N	\N	3.173200	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	ba2cc9bf-46ad-43b0-bd3e-0795c80cf5c2
runyourai	gpu	L20	48.00	\N	\N	7.241300	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	881634f2-5f85-4bc9-850a-a0e9582742e8
runyourai	gpu	L20	48.00	\N	\N	3.300700	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	67fe79ad-dac1-4c5e-9799-f81a9c50dd1b
runyourai	gpu	L20	48.00	\N	\N	3.620300	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	1b7938a9-5f6b-4e05-b4e5-67d9473c3c2f
runyourai	gpu	RTX	0.00	\N	\N	1.176800	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	74b02c8b-b0e6-42b1-876a-c0c3f956c471
runyourai	gpu	A10	24.00	\N	\N	4.873200	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	2ad1fcaa-24d3-431b-ad8f-72a52d0285b1
runyourai	gpu	A10	24.00	\N	\N	3.508700	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	7c9b0e10-2e6e-481c-acca-68d891ea2b35
runyourai	gpu	A10	24.00	\N	\N	2.436200	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	b099012e-10fe-43db-992e-3e68c3707c08
runyourai	gpu	A10	24.00	\N	\N	2.923900	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	f0ae7b6d-5bab-4142-b768-623510dbcc80
runyourai	gpu	A10	24.00	\N	\N	2.071000	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	9f4d3ca4-77dc-466e-a992-dda34592d55b
runyourai	gpu	A10	24.00	\N	\N	2.192800	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	c1547dd6-fd61-4f80-870c-ad2928a91b09
runyourai	gpu	A100	80.00	\N	\N	2.617400	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	0c7c3d3c-7d80-4c88-957c-3fc5ad5833f4
runyourai	gpu	A100	40.00	\N	\N	2.202200	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	9a687e2e-098e-40cc-9b52-a035a4202a59
runyourai	gpu	P100	16.00	\N	\N	2.688400	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	cad6c09d-0e57-4e40-9f6d-f482af56d62d
runyourai	gpu	P100	16.00	\N	\N	2.232600	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	66b6278d-041c-413f-a65d-bc96744d06b8
runyourai	gpu	P100	16.00	\N	\N	4.171000	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	146b8363-0a90-4479-beae-af64f001e626
runyourai	gpu	H100	94.00	\N	\N	5.072500	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	daecd723-7d44-4514-bfbc-e584194e3c15
runyourai	gpu	L40S	48.00	\N	\N	2.753600	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:29:26+00	8f956734-45a6-4d8a-95d3-7e50b5a1ec85
runpod	gpu	MI300X	192.00	\N	\N	2.390000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	4b352faa-a307-4b46-8b71-46f78dee8a84
runpod	gpu	A100 PCIE	80.00	\N	\N	1.390000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	e3c253a1-d1f3-470d-8450-1061992545b4
runpod	gpu	A100 SXM 40GB	40.00	\N	\N	1.000000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	c3fed99b-45a3-4673-92e1-07c9dbbcacd5
runpod	gpu	A100 SXM	80.00	\N	\N	1.490000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	ec1113fc-d14d-44d8-ab10-9c417c611c7d
runpod	gpu	A40	48.00	\N	\N	0.440000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	4fe75f6c-63d9-45e4-bfe7-2a6fb8fa4954
runpod	gpu	B200	180.00	\N	\N	5.890000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	3098d516-27c4-4a0e-bda2-d73cfff821be
runpod	gpu	B300	288.00	\N	\N	7.390000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	fd7f41f6-0c75-496d-a0da-93861c1f0dcb
runpod	gpu	NVIDIA GEFORCE GTX 1050 TI	4.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	d844fd88-a293-484e-900c-9aa18322107c
runpod	gpu	RTX 3070	8.00	\N	\N	0.130000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	b026196a-a69b-4fdd-ae2e-b140bfbc4f23
runpod	gpu	RTX 3080	10.00	\N	\N	0.170000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	f7dcd6b0-439d-4b6e-a1b9-336442d0bdde
runpod	gpu	RTX 3080 TI	12.00	\N	\N	0.180000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	68838dbf-cb89-475b-a0af-52b86d8988b8
runpod	gpu	RTX 3090	24.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	a2246b3a-3578-434d-8879-b7ab48430024
runpod	gpu	RTX 3090 TI	24.00	\N	\N	0.460000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	48936d1c-b5ad-43fb-bcad-00878540c7ec
runpod	gpu	RTX 4070 TI	12.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	f6270a64-9f9a-4dc6-9802-381914187d93
runpod	gpu	RTX 4080	16.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	ef63bd90-f5a6-4e0e-b01e-e7c90ea31e4e
runpod	gpu	RTX 4080 SUPER	16.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	d19cee8c-974d-46bb-afd0-65af5d08d3a2
runpod	gpu	RTX 4090	24.00	\N	\N	0.690000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	cb54bc69-5251-440c-ac29-d68ff87b15ba
runpod	gpu	RTX 5080	16.00	\N	\N	0.590000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	a8a8b9f2-b4e1-47e0-a7a1-d4d27bb55ba2
runpod	gpu	RTX 5090	32.00	\N	\N	0.990000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	bac3b95e-9e6e-408e-a25a-2291d019ef45
runpod	gpu	H100 SXM	80.00	\N	\N	2.990000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	33c66584-4a11-41c7-81d1-7b7998361b11
runpod	gpu	H100 NVL	94.00	\N	\N	3.190000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	c56825e2-4df6-42ba-b9b7-3cffcfe22951
runpod	gpu	H100 PCIE	80.00	\N	\N	2.890000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	0bb3132e-c20b-4095-aceb-4a3237b3d45f
runpod	gpu	H200 SXM	141.00	\N	\N	4.390000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	74d58627-92d8-4aeb-8821-6bde3d0fd2a6
runpod	gpu	H200 NVL	143.00	\N	\N	3.790000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	bcb141bf-1b90-4981-a440-6ea534747015
runpod	gpu	L4	24.00	\N	\N	0.390000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	39accb20-702f-4633-8d06-e5df2039f3e8
runpod	gpu	L40	48.00	\N	\N	0.820000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	674d1361-8e8f-4b65-8bc1-42b940b0ccf7
runpod	gpu	L40S	48.00	\N	\N	0.990000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	b158525e-d77c-4c9a-9881-c6a67b4a2fa0
runpod	gpu	RTX 2000 ADA	16.00	\N	\N	0.240000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	c2bbc2c5-d53e-4467-9c9b-efe02512d883
runpod	gpu	RTX 4000 ADA	20.00	\N	\N	0.280000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	e724ff82-8b2f-4c50-9e46-d674c0930bb1
runpod	gpu	RTX 4000 ADA SFF	20.00	\N	\N	0.440000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	2c4ab7cb-5f57-4bc4-b6e2-b47ca0900131
runpod	gpu	RTX 5000 ADA	32.00	\N	\N	0.830000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	72080d1a-f005-4167-96f3-e5ef702f669c
runpod	gpu	RTX 6000 ADA	48.00	\N	\N	0.840000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	ac3fc533-ac3e-40f1-ba4b-cd3f326acbb2
runpod	gpu	RTX A2000	6.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	77746581-49ee-42a7-ab6b-765d4b4bb540
runpod	gpu	RTX A4000	16.00	\N	\N	0.250000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	f32d880a-9d31-47f3-8b65-d70a9103ad4b
runpod	gpu	RTX A4500	20.00	\N	\N	0.250000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	c3ad9118-6fc0-47d8-9ab0-09ac46de9eda
runpod	gpu	RTX A5000	24.00	\N	\N	0.270000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	44357fc1-c6a8-4e19-8284-af6105ab8bd9
runpod	gpu	RTX A6000	48.00	\N	\N	0.530000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	2d783440-9ca4-4bbc-b7fe-251d22d51699
runpod	gpu	RTX PRO 4000	24.00	\N	\N	0.570000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	2522a5ef-1f6f-4dfa-ba94-b7dc6cf27d12
runpod	gpu	RTX PRO 4500	32.00	\N	\N	0.740000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	636fd407-6e9a-4671-b739-a271f987453f
runpod	gpu	RTX PRO 5000	48.00	\N	\N	0.960000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	1c8311aa-b723-493b-8176-37aff76190d5
runpod	gpu	RTX PRO 6000 MAXQ	96.00	\N	\N	0.500000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	44cbf1af-6bd7-4ba8-9230-7844ea0fe68b
runpod	gpu	RTX PRO 6000	96.00	\N	\N	1.990000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	0389b323-4971-42a6-a263-422603f71182
runpod	gpu	PRO 6000 MIG 24GB	24.00	\N	\N	0.490000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	e2800c65-5e6e-44c7-a78b-72c9d4e34a46
runpod	gpu	PRO 6000 MIG 48GB	48.00	\N	\N	1.000000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	1ec66608-86a2-4659-a888-40caa2c87ff4
runpod	gpu	RTX PRO 6000 WK	96.00	\N	\N	1.890000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	b3e415d8-f1e9-4a0e-b1c2-39d2ed9b1f13
runpod	gpu	TESLA V100	16.00	\N	\N	0.190000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	43a79df0-06a2-4bc4-8660-781309b236e4
runpod	gpu	V100 SXM2	16.00	\N	\N	0.230000	available	https://www.runpod.io/console/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	2a7046cc-9f3e-4ded-9ed6-65d6416bda90
aws	gpu	L40S	0.00	\N	\N	2.288000	available	https://aws.amazon.com/ec2/instance-types/g6e/	\N	\N	2026-07-23 10:59:31+00	adf2dc42-f527-4cea-b1fe-9b7f5c6e49ee
aws	gpu	L40S	0.00	\N	\N	18.522300	available	https://aws.amazon.com/ec2/instance-types/g6e/	\N	\N	2026-07-23 10:59:31+00	250df37a-a0be-4b29-91ee-bb3ce0bedd41
aws	gpu	L4	0.00	\N	\N	23.658200	available	https://aws.amazon.com/ec2/instance-types/g6/	\N	\N	2026-07-23 10:59:31+00	ab261f6a-9d82-4804-8d31-40d9745151fd
aws	gpu	T4	0.00	\N	\N	0.925000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	\N	\N	2026-07-23 10:59:31+00	621c5918-fc98-489b-9a2e-bc42fc17c13f
aws	gpu	L4	0.00	\N	\N	44.208000	available	https://aws.amazon.com/ec2/instance-types/g6/	\N	\N	2026-07-23 10:59:31+00	0c4a2217-e74c-426c-88f1-27674e669be1
aws	gpu	UNKNOWN GPU	0.00	\N	\N	0.719300	available	https://aws.amazon.com/ec2/instance-types/g6f/	\N	\N	2026-07-23 10:59:31+00	85c7227b-5822-421b-92d0-464ad79b25a9
aws	gpu	A10G	0.00	\N	\N	1.996900	available	https://aws.amazon.com/ec2/instance-types/g5/	\N	\N	2026-07-23 10:59:31+00	093214ee-9605-41b0-87ef-bfa929ea28f2
aws	gpu	V100	0.00	\N	\N	33.872000	available	https://aws.amazon.com/ec2/instance-types/p3/	\N	\N	2026-07-23 10:59:31+00	f12894c5-9a93-4c4d-a746-8650a3ee3f4f
aws	gpu	L4	0.00	\N	\N	2.162100	available	https://aws.amazon.com/ec2/instance-types/g6/	\N	\N	2026-07-23 10:59:31+00	5735dad9-7cd5-455a-9503-f1a255ab888e
aws	gpu	L40S	0.00	\N	\N	2.756500	available	https://aws.amazon.com/ec2/instance-types/g6e/	\N	\N	2026-07-23 10:59:31+00	fcbdbe5c-b196-4371-a4dd-22801e7ebace
aws	gpu	L4	0.00	\N	\N	1.469600	available	https://aws.amazon.com/ec2/instance-types/g6/	\N	\N	2026-07-23 10:59:31+00	27a615f9-064d-48aa-859a-28661495d1db
aws	gpu	UNKNOWN GPU	0.00	\N	\N	0.292000	available	https://aws.amazon.com/ec2/instance-types/g6f/	\N	\N	2026-07-23 10:59:31+00	c89d3b11-399a-4dbe-86a4-3ed0cf8531e3
aws	gpu	L4	0.00	\N	\N	3.017700	available	https://aws.amazon.com/ec2/instance-types/g6/	\N	\N	2026-07-23 10:59:31+00	c7acb3c6-3320-46e9-83ad-07f0c0c036b6
aws	gpu	UNKNOWN GPU	0.00	\N	\N	0.248400	available	https://aws.amazon.com/ec2/instance-types/g6f/	\N	\N	2026-07-23 10:59:31+00	c1cedef4-d2a0-45d0-bd2a-5d7003d00d81
aws	gpu	A10G	0.00	\N	\N	3.010100	available	https://aws.amazon.com/ec2/instance-types/g5/	\N	\N	2026-07-23 10:59:31+00	5e27b0ff-cf2c-42f0-8b4b-f86dd2ba9164
aws	gpu	UNKNOWN GPU	0.00	\N	\N	1.018500	available	https://aws.amazon.com/ec2/instance-types/g5g/	\N	\N	2026-07-23 10:59:31+00	2cfcadad-0b6e-4f92-94df-f2f6628f688d
aws	gpu	L4	0.00	\N	\N	5.258400	available	https://aws.amazon.com/ec2/instance-types/g6/	\N	\N	2026-07-23 10:59:31+00	56ba9382-04d0-4aef-a441-b53d5f924e8d
aws	gpu	V100	0.00	\N	\N	4.234000	available	https://aws.amazon.com/ec2/instance-types/p3/	\N	\N	2026-07-23 10:59:31+00	7f1a5a65-7d60-4046-b5fd-8d5a942c008e
aws	gpu	T4	0.00	\N	\N	1.481000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	\N	\N	2026-07-23 10:59:31+00	adf301bb-ce0e-4b63-8b75-a264845c8259
aws	gpu	UNKNOWN GPU	0.00	\N	\N	0.683900	available	https://aws.amazon.com/ec2/instance-types/g5g/	\N	\N	2026-07-23 10:59:31+00	677751dd-c938-4a42-81cb-c01e45e35a24
aws	gpu	UNKNOWN GPU	0.00	\N	\N	1.687600	available	https://aws.amazon.com/ec2/instance-types/g5g/	\N	\N	2026-07-23 10:59:31+00	d6e7bb8e-73b8-414d-889b-43db2b6606bc
aws	gpu	UNKNOWN GPU	0.00	\N	\N	3.375200	available	https://aws.amazon.com/ec2/instance-types/g5g/	\N	\N	2026-07-23 10:59:31+00	b9b12a4f-b610-4030-a4c3-013c0cfa4ab5
aws	gpu	T4	0.00	\N	\N	0.647000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	\N	\N	2026-07-23 10:59:31+00	2565b048-9dc6-4a59-b64a-296f248ff7c4
aws	gpu	T4	0.00	\N	\N	4.812000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	\N	\N	2026-07-23 10:59:31+00	4c617c4d-6fbd-43ab-a440-7dfdfaa7d6bd
aws	gpu	T4	0.00	\N	\N	5.353000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	\N	\N	2026-07-23 10:59:31+00	ebc8ad19-9ed0-4781-bb23-56b3befcce1b
aws	gpu	T4	0.00	\N	\N	9.624000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	\N	\N	2026-07-23 10:59:31+00	a887cbe6-f379-4b70-a933-d1c56ef202a7
aws	gpu	A10G	0.00	\N	\N	6.974400	available	https://aws.amazon.com/ec2/instance-types/g5/	\N	\N	2026-07-23 10:59:31+00	e3200105-8925-448e-ad99-473bc91c8e1f
aws	gpu	UNKNOWN GPU	0.00	\N	\N	7.168100	available	https://aws.amazon.com/ec2/instance-types/g6f/	\N	\N	2026-07-23 10:59:31+00	6abff25f-6363-4591-8ed7-ccee48a667dd
aws	gpu	A10G	0.00	\N	\N	10.014000	available	https://aws.amazon.com/ec2/instance-types/g5/	\N	\N	2026-07-23 10:59:31+00	aead90ce-4ba6-4b16-9a9d-05c12769f8fb
aws	gpu	V100	0.00	\N	\N	16.936000	available	https://aws.amazon.com/ec2/instance-types/p3/	\N	\N	2026-07-23 10:59:31+00	b24d8afc-f4f4-4710-9924-cd9c72c46b19
aws	gpu	L4	0.00	\N	\N	19.660800	available	https://aws.amazon.com/ec2/instance-types/g6/	\N	\N	2026-07-23 10:59:31+00	3eca8855-01ad-42c3-969d-c0e9bc2d8864
aws	gpu	T4	0.00	\N	\N	2.677000	available	https://aws.amazon.com/ec2/instance-types/g4dn/	\N	\N	2026-07-23 10:59:31+00	8cf96055-e464-4a31-9c94-5229cc458f48
aws	gpu	UNKNOWN GPU	0.00	\N	\N	87.348500	available	https://aws.amazon.com/ec2/instance-types/p5en/	\N	\N	2026-07-23 10:59:31+00	bf67567d-5351-436a-a61c-b760ea6937cc
aws	gpu	A10G	0.00	\N	\N	5.036500	available	https://aws.amazon.com/ec2/instance-types/g5/	\N	\N	2026-07-23 10:59:31+00	154fa913-b47c-4cde-8c25-f2cba4828aa4
aws	gpu	L40S	0.00	\N	\N	12.900100	available	https://aws.amazon.com/ec2/instance-types/g6e/	\N	\N	2026-07-23 10:59:31+00	0200c54a-e906-4213-a626-c53725bb85c9
aws	gpu	L4	0.00	\N	\N	7.627000	available	https://aws.amazon.com/ec2/instance-types/g6/	\N	\N	2026-07-23 10:59:31+00	9029fc46-b608-4135-a274-9e59697dfdb6
aws	gpu	H100	0.00	\N	\N	75.955200	available	https://aws.amazon.com/ec2/instance-types/p5/	\N	\N	2026-07-23 10:59:31+00	3169fd3f-d2bc-4930-9068-97105e31357a
aws	gpu	UNKNOWN GPU	0.00	\N	\N	3.375200	available	https://aws.amazon.com/ec2/instance-types/g5g/	\N	\N	2026-07-23 10:59:31+00	e55ca1f7-b757-46a4-9ca8-81c7d3d5841c
aws	gpu	A100	0.00	\N	\N	30.410300	available	https://aws.amazon.com/ec2/instance-types/p4d/	\N	\N	2026-07-23 10:59:31+00	134baba9-2853-49b9-bc43-4516c5812c07
aws	gpu	UNKNOWN GPU	0.00	\N	\N	0.516600	available	https://aws.amazon.com/ec2/instance-types/g5g/	\N	\N	2026-07-23 10:59:31+00	a678177d-31e5-42eb-bfb6-67c20cb18d78
aws	gpu	A10G	0.00	\N	\N	1.490300	available	https://aws.amazon.com/ec2/instance-types/g5/	\N	\N	2026-07-23 10:59:31+00	6d06dd52-7439-44f4-85ee-49f916b4e529
aws	gpu	L40S	0.00	\N	\N	37.044700	available	https://aws.amazon.com/ec2/instance-types/g6e/	\N	\N	2026-07-23 10:59:31+00	d0339e11-22b1-419c-811a-b8816060b985
aws	gpu	A10G	0.00	\N	\N	1.237000	available	https://aws.amazon.com/ec2/instance-types/g5/	\N	\N	2026-07-23 10:59:31+00	7d080305-cda7-4da4-be09-fc6a7fe824ef
aws	gpu	L40S	0.00	\N	\N	3.693600	available	https://aws.amazon.com/ec2/instance-types/g6e/	\N	\N	2026-07-23 10:59:31+00	a383df4e-5d33-4d9e-8e6c-2a273bfc3847
aws	gpu	L40S	0.00	\N	\N	5.567600	available	https://aws.amazon.com/ec2/instance-types/g6e/	\N	\N	2026-07-23 10:59:31+00	331e094a-7143-4893-8c2a-9f2a2991f80f
aws	gpu	A10G	0.00	\N	\N	20.028100	available	https://aws.amazon.com/ec2/instance-types/g5/	\N	\N	2026-07-23 10:59:31+00	910348f1-ca91-40c6-a6db-09516c7be220
aws	gpu	INFERENTIA2	0.00	\N	\N	0.909800	available	https://aws.amazon.com/ec2/instance-types/inf2/	\N	\N	2026-07-23 10:59:31+00	885302d2-a71c-45a0-8fe8-7787a2b479de
aws	gpu	L40S	0.00	\N	\N	9.315700	available	https://aws.amazon.com/ec2/instance-types/g6e/	\N	\N	2026-07-23 10:59:31+00	46eb210b-99be-43b0-aaf6-c347b7173661
vessl	gpu	B300	288.00	\N	\N	7.290000	available	https://vessl.ai/ko/pricing	\N	\N	2026-07-23 10:59:31+00	d546af64-e0fe-48cd-91b8-1e11123f7902
vessl	gpu	B200	192.00	\N	\N	5.790000	available	https://vessl.ai/ko/pricing	\N	\N	2026-07-23 10:59:31+00	9ef3b728-5021-4998-896a-c2eeddf97284
vessl	gpu	H200 SXM	141.00	\N	\N	4.290000	available	https://vessl.ai/ko/pricing	\N	\N	2026-07-23 10:59:31+00	a9134192-c52c-47e5-9948-4734d4e7f210
vessl	gpu	H100 SXM	80.00	\N	\N	3.190000	available	https://vessl.ai/ko/pricing	\N	\N	2026-07-23 10:59:31+00	765322ea-0867-4dfe-97b9-206abf9332c3
vessl	gpu	A100 SXM	80.00	\N	\N	1.390000	available	https://vessl.ai/ko/pricing	\N	\N	2026-07-23 10:59:31+00	16b6171c-0765-4933-a664-1ff12178698e
vessl	gpu	L40S	48.00	\N	\N	1.800000	available	https://vessl.ai/ko/pricing	\N	\N	2026-07-23 10:59:31+00	74378747-5d27-4763-bdc0-53645b4bd923
gpuaas	gpu	H100 SXM	80.00	\N	\N	2.390000	available	https://gpuaas.kr/	\N	\N	2026-07-23 10:59:31+00	1de5f1bf-5e95-433c-8a0e-cb1504555284
gpuaas	gpu	H100 SXM (연간계약)	80.00	\N	\N	2.200000	available	https://gpuaas.kr/	\N	\N	2026-07-23 10:59:31+00	48a8d225-fabe-417f-bcf6-ce041936923a
cloudv	gpu	A100 40GB	40.00	\N	\N	0.188400	available	https://cloudv.kr/server/gpu.html	\N	\N	2026-07-23 10:59:31+00	22c6fdff-6716-4d6f-8c30-7148b713ae65
cloudv	gpu	A100 40GB	40.00	\N	\N	0.312500	available	https://cloudv.kr/server/gpu.html	\N	\N	2026-07-23 10:59:31+00	ffc0062a-fdc7-4c4c-b054-0f0a385e01a1
cloudv	gpu	A100 40GB	40.00	\N	\N	0.560700	available	https://cloudv.kr/server/gpu.html	\N	\N	2026-07-23 10:59:31+00	1461b92b-674f-4e72-bba2-6705e11c07f2
cloudv	gpu	A100 80GB	80.00	\N	\N	0.226100	available	https://cloudv.kr/server/gpu.html	\N	\N	2026-07-23 10:59:31+00	d1b7cb1d-7d38-4795-8d08-f80651760557
cloudv	gpu	A100 80GB	80.00	\N	\N	0.375000	available	https://cloudv.kr/server/gpu.html	\N	\N	2026-07-23 10:59:31+00	a943b982-cf76-464d-9445-fd78fe9c80ba
cloudv	gpu	A100 80GB	80.00	\N	\N	0.672800	available	https://cloudv.kr/server/gpu.html	\N	\N	2026-07-23 10:59:31+00	347d0436-3ef5-4865-9e07-5fd0cbd6b2c7
cloudv	gpu	PRO 5000	48.00	\N	\N	0.188400	available	https://cloudv.kr/server/gpu.html	\N	\N	2026-07-23 10:59:31+00	22f8065c-ab46-497a-9811-d24941ef8d50
cloudv	gpu	PRO 6000	96.00	\N	\N	0.188400	available	https://cloudv.kr/server/gpu.html	\N	\N	2026-07-23 10:59:31+00	2f928456-4405-41e3-969d-b396b7a0e299
cloudv	gpu	RTX 5060	16.00	\N	\N	0.120900	available	https://cloudv.kr/server/gpu.html	\N	\N	2026-07-23 10:59:31+00	624ef406-90b1-4cdb-bb9d-68ac538c0dab
cloudv	gpu	RTX 5090	32.00	\N	\N	0.262400	available	https://cloudv.kr/server/gpu.html	\N	\N	2026-07-23 10:59:31+00	8ca3237f-cf92-445e-a183-7cfa6ae96657
runyourai	gpu	H100	80.00	\N	\N	2.619600	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	d2b91553-1272-48ee-9bfe-893e7a4a22d9
runyourai	gpu	B200	192.00	\N	\N	6.776100	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	38404583-2ace-44aa-9721-13fee70b9d0e
runyourai	gpu	L40S	48.00	\N	\N	1.232600	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	68b33f2e-192c-45f8-bcd0-fd19258f65a8
runyourai	gpu	RTX	0.00	\N	\N	0.817400	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	982a58df-eaf9-40d9-9206-34ada50b112b
runyourai	gpu	RTX	0.00	\N	\N	0.540600	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	6f8d31fe-1362-449e-8f5c-d15d47168c54
runyourai	gpu	RTX	0.00	\N	\N	0.913800	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	d0342c96-deb6-46eb-92c5-78f6bfe679d9
runyourai	gpu	A100	80.00	\N	\N	1.925400	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	c6d47b26-eb54-40f4-97af-60f81254f687
runyourai	gpu	A100	40.00	\N	\N	1.454300	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	031d20d3-3552-4aa3-9bdb-024c6608c5c1
runyourai	gpu	RTX	0.00	\N	\N	0.332600	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	34ca7b31-ca0b-41cf-b601-ab7b093cb455
runyourai	gpu	L40S	48.00	\N	\N	1.509400	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	01f0d335-38be-484f-ba23-5b01e1bd65ca
runyourai	gpu	H200	80.00	\N	\N	4.004300	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	2d2d3ae3-8225-4468-a012-7964d53755e1
runyourai	gpu	H100	80.00	\N	\N	3.173200	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	69364dcd-553d-4fe4-8ca4-63f5a4ce6532
runyourai	gpu	L20	48.00	\N	\N	7.241300	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	1d2bee9a-79e7-4a52-a87d-f3a991b2178d
runyourai	gpu	L20	48.00	\N	\N	3.300700	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	3d00d92a-07f1-4527-8e0b-72e4438c7054
runyourai	gpu	L20	48.00	\N	\N	3.620300	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	8131c97a-c0c1-4299-913d-fee059b2ea26
runyourai	gpu	RTX	0.00	\N	\N	1.176800	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	a2a958d6-08ed-4305-b7cc-201fbe1b09e6
runyourai	gpu	A10	24.00	\N	\N	4.873200	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	d916a0ac-c145-4375-9e52-9c0c30e4d472
runyourai	gpu	A10	24.00	\N	\N	3.508700	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	0e8c304a-85fc-45dc-a966-903514351f50
runyourai	gpu	A10	24.00	\N	\N	2.436200	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	64217486-b0cf-425a-812f-0f7bbfc02358
runyourai	gpu	A10	24.00	\N	\N	2.923900	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	adac4391-adba-409e-8c4b-987ea240c946
runyourai	gpu	A10	24.00	\N	\N	2.071000	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	9f4433bb-3e3c-4b90-a5af-71930d1f5096
runyourai	gpu	A10	24.00	\N	\N	2.192800	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	4fd0dacd-6095-4fa2-91c9-5a6fbcea42df
runyourai	gpu	A100	80.00	\N	\N	2.617400	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	3f285d16-9e0f-4278-9f0f-37f9508ef701
runyourai	gpu	A100	40.00	\N	\N	2.202200	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	c6eeed60-9fa6-4472-8707-7247b7b7a693
runyourai	gpu	P100	16.00	\N	\N	2.688400	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	d7e047cf-d3b2-4b2e-98e3-2db6020ca145
runyourai	gpu	P100	16.00	\N	\N	2.232600	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	f0525ec1-5bd6-4c57-9735-55a5a3761097
runyourai	gpu	P100	16.00	\N	\N	4.171000	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	330e882f-eb05-42e3-89bb-8d204e31a8f6
runyourai	gpu	H100	94.00	\N	\N	5.072500	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	626f6c23-c12d-4e22-aefe-c568db3a21f9
runyourai	gpu	L40S	48.00	\N	\N	2.753600	available	https://console.runyour.ai/gpu-cloud	\N	\N	2026-07-23 10:59:31+00	c0c8efa9-8a1f-4b67-8d81-74d8a7206ffa
ncloud	gpu	L40S	48.00	\N	\N	3.122500	available	https://www.ncloud.com/product/compute/gpuServer	\N	\N	2026-07-23 10:59:31+00	383361cb-7245-4c3a-ace3-8bb2712d1667
ncloud	gpu	L40S	48.00	\N	\N	3.988400	available	https://www.ncloud.com/product/compute/gpuServer	\N	\N	2026-07-23 10:59:31+00	0db0ed36-2882-4504-940d-25308992109f
ncloud	gpu	L40S	48.00	\N	\N	6.244200	available	https://www.ncloud.com/product/compute/gpuServer	\N	\N	2026-07-23 10:59:31+00	8bf94ac2-1b00-4757-bdbe-a1a9eb565611
ncloud	gpu	L40S	48.00	\N	\N	7.976100	available	https://www.ncloud.com/product/compute/gpuServer	\N	\N	2026-07-23 10:59:31+00	445f2d6c-2b05-4a01-9761-be0748a2000f
ncloud	gpu	L40S	48.00	\N	\N	11.884800	available	https://www.ncloud.com/product/compute/gpuServer	\N	\N	2026-07-23 10:59:31+00	ab4be563-4e84-42b9-82e5-8d38315bc9ce
ncloud	gpu	L40S	48.00	\N	\N	15.059400	available	https://www.ncloud.com/product/compute/gpuServer	\N	\N	2026-07-23 10:59:31+00	3e2ce8b8-238f-41dd-9b3d-2a5b6426357a
ncloud	gpu	L4	24.00	\N	\N	1.048600	available	https://www.ncloud.com/product/compute/gpuServer	\N	\N	2026-07-23 10:59:31+00	6f4ffbba-c1ca-42a2-bc3d-f411be2f512b
ncloud	gpu	A100	80.00	\N	\N	36.179700	available	https://www.ncloud.com/product/compute/gpuServer	\N	\N	2026-07-23 10:59:31+00	b50f24ea-48f7-4361-b7c3-cb3d41c61d82
ncloud	gpu	V100	32.00	\N	\N	3.102200	available	https://www.ncloud.com/product/compute/gpuServer	\N	\N	2026-07-23 10:59:31+00	ee143b40-802f-4792-8bc2-5846acb151a2
ncloud	gpu	V100	32.00	\N	\N	6.207200	available	https://www.ncloud.com/product/compute/gpuServer	\N	\N	2026-07-23 10:59:31+00	996dfb1b-b52a-4d6d-857e-4125cd98e417
ncloud	gpu	V100	32.00	\N	\N	12.417400	available	https://www.ncloud.com/product/compute/gpuServer	\N	\N	2026-07-23 10:59:31+00	828519c9-1dd2-4d68-b310-e88bf71ec843
unknown	gpu	UNKNOWN	0.00	\N	\N	212.060000	AVAILABLE	\N	\N	\N	2026-07-23 10:29:26+00	ee352402-e522-411b-90c6-758c56925f09
unknown	gpu	UNKNOWN	0.00	\N	\N	552.330000	AVAILABLE	\N	\N	\N	2026-07-23 10:29:26+00	af22c8de-4f84-4ca9-9d2f-61e2e2c83cad
unknown	gpu	UNKNOWN	0.00	\N	\N	1385.357143	AVAILABLE	\N	\N	\N	2026-07-23 10:29:26+00	a96bdfe1-207a-4299-a92d-4ef431771ff4
unknown	gpu	UNKNOWN	0.00	\N	\N	193.750000	AVAILABLE	\N	\N	\N	2026-07-23 10:29:26+00	17924c4f-026c-4bb4-a039-634e3c7dc8e0
unknown	gpu	UNKNOWN	0.00	\N	\N	556.670000	AVAILABLE	\N	\N	\N	2026-07-23 10:29:26+00	35691e9d-b4d1-4ffa-97cd-206a68b3cd6d
unknown	gpu	UNKNOWN	0.00	\N	\N	102.620000	AVAILABLE	\N	\N	\N	2026-07-23 10:29:26+00	f132ac0a-0384-4fb4-a706-836385355cda
unknown	gpu	UNKNOWN	0.00	\N	\N	959.480000	AVAILABLE	\N	\N	\N	2026-07-23 10:29:26+00	fc1a7bf1-bca6-4ce8-aea7-1bf98c6ea771
unknown	gpu	UNKNOWN	0.00	\N	\N	421.210000	AVAILABLE	\N	\N	\N	2026-07-23 10:29:26+00	e6d5b203-8a44-4a98-ac2f-f47cc1ddbae2
unknown	gpu	UNKNOWN	0.00	\N	\N	553.920000	AVAILABLE	\N	\N	\N	2026-07-23 10:29:26+00	b3301891-880b-4c4b-aaff-5a815628b8d7
unknown	gpu	UNKNOWN	0.00	\N	\N	212.060000	AVAILABLE	\N	\N	\N	2026-07-23 10:59:31+00	c59fb8d2-c209-45fd-ba00-c709d5b22f6e
unknown	gpu	UNKNOWN	0.00	\N	\N	552.330000	AVAILABLE	\N	\N	\N	2026-07-23 10:59:31+00	061e05ba-853c-44b6-99ce-c17692cff95d
unknown	gpu	UNKNOWN	0.00	\N	\N	1365.714286	AVAILABLE	\N	\N	\N	2026-07-23 10:59:31+00	b1e618a9-2700-47dd-a414-57c56d8f5297
unknown	gpu	UNKNOWN	0.00	\N	\N	192.857143	AVAILABLE	\N	\N	\N	2026-07-23 10:59:31+00	c8e93390-cf26-43d5-94a7-63f47f062b48
unknown	gpu	UNKNOWN	0.00	\N	\N	556.670000	AVAILABLE	\N	\N	\N	2026-07-23 10:59:31+00	48703ac1-edc7-4c66-970e-1a6d2b763bba
unknown	gpu	UNKNOWN	0.00	\N	\N	102.620000	AVAILABLE	\N	\N	\N	2026-07-23 10:59:31+00	e6af3974-e5bc-429f-a528-8c74c9bab8c3
unknown	gpu	UNKNOWN	0.00	\N	\N	959.480000	AVAILABLE	\N	\N	\N	2026-07-23 10:59:31+00	acd3a6b2-e42f-4e55-a53d-bae1f0a50ae9
unknown	gpu	UNKNOWN	0.00	\N	\N	421.210000	AVAILABLE	\N	\N	\N	2026-07-23 10:59:31+00	6aa4de2c-23d4-4bd9-86cd-a9675e6b3a33
unknown	gpu	UNKNOWN	0.00	\N	\N	553.920000	AVAILABLE	\N	\N	\N	2026-07-23 10:59:31+00	06c69427-29ee-4e59-a587-b85b0fda33de
\.


--
-- Data for Name: tbl_news_arti; Type: TABLE DATA; Schema: public; Owner: infraindex
--

COPY public.tbl_news_arti (titl_nm, arti_url, src_nm, pub_ts, sum_txt, kwd_txt, clct_tr, crt_ts, id) FROM stdin;
\.


--
-- Data for Name: tbl_obx_evt; Type: TABLE DATA; Schema: public; Owner: infraindex
--

COPY public.tbl_obx_evt (tpc_nm, evt_typ, payld_dat, crt_ts, proc_st, proc_ts, id) FROM stdin;
\.


--
-- Data for Name: tbl_rtl_prc_hist; Type: TABLE DATA; Schema: public; Owner: infraindex
--

COPY public.tbl_rtl_prc_hist (pltf_nm, hw_typ, mfg_nm, mdl_nm, capa_gb, prc_amt, crncy_cd, prd_url, is_offc, ts, id) FROM stdin;
\.


--
-- Name: SYS_CD_BAS SYS_CD_BAS_pkey; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public."SYS_CD_BAS"
    ADD CONSTRAINT "SYS_CD_BAS_pkey" PRIMARY KEY ("SYS_GROUP_ID", "SYS_CD_ID");


--
-- Name: SYS_CD_GROUP_BAS SYS_CD_GROUP_BAS_pkey; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public."SYS_CD_GROUP_BAS"
    ADD CONSTRAINT "SYS_CD_GROUP_BAS_pkey" PRIMARY KEY ("SYS_GROUP_ID");


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: collection_runs collection_runs_pkey; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.collection_runs
    ADD CONSTRAINT collection_runs_pkey PRIMARY KEY (id);


--
-- Name: cpu_manufacturers cpu_manufacturers_name_key; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.cpu_manufacturers
    ADD CONSTRAINT cpu_manufacturers_name_key UNIQUE (name);


--
-- Name: cpu_manufacturers cpu_manufacturers_pkey; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.cpu_manufacturers
    ADD CONSTRAINT cpu_manufacturers_pkey PRIMARY KEY (id);


--
-- Name: cpu_models cpu_models_name_key; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.cpu_models
    ADD CONSTRAINT cpu_models_name_key UNIQUE (name);


--
-- Name: cpu_models cpu_models_pkey; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.cpu_models
    ADD CONSTRAINT cpu_models_pkey PRIMARY KEY (id);


--
-- Name: cpu_variants cpu_variants_pkey; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.cpu_variants
    ADD CONSTRAINT cpu_variants_pkey PRIMARY KEY (id);


--
-- Name: data_licenses data_licenses_pkey; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.data_licenses
    ADD CONSTRAINT data_licenses_pkey PRIMARY KEY (id);


--
-- Name: data_quality_issues data_quality_issues_pkey; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.data_quality_issues
    ADD CONSTRAINT data_quality_issues_pkey PRIMARY KEY (id);


--
-- Name: gpu_manufacturers gpu_manufacturers_name_key; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.gpu_manufacturers
    ADD CONSTRAINT gpu_manufacturers_name_key UNIQUE (name);


--
-- Name: gpu_manufacturers gpu_manufacturers_pkey; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.gpu_manufacturers
    ADD CONSTRAINT gpu_manufacturers_pkey PRIMARY KEY (id);


--
-- Name: gpu_models gpu_models_name_key; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.gpu_models
    ADD CONSTRAINT gpu_models_name_key UNIQUE (name);


--
-- Name: gpu_models gpu_models_pkey; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.gpu_models
    ADD CONSTRAINT gpu_models_pkey PRIMARY KEY (id);


--
-- Name: gpu_variants gpu_variants_pkey; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.gpu_variants
    ADD CONSTRAINT gpu_variants_pkey PRIMARY KEY (id);


--
-- Name: idempotency_keys idempotency_keys_pkey; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.idempotency_keys
    ADD CONSTRAINT idempotency_keys_pkey PRIMARY KEY (id);


--
-- Name: instance_offerings instance_offerings_pkey; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.instance_offerings
    ADD CONSTRAINT instance_offerings_pkey PRIMARY KEY (id);


--
-- Name: memory_manufacturers memory_manufacturers_pkey; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.memory_manufacturers
    ADD CONSTRAINT memory_manufacturers_pkey PRIMARY KEY (id);


--
-- Name: memory_modules memory_modules_pkey; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.memory_modules
    ADD CONSTRAINT memory_modules_pkey PRIMARY KEY (id);


--
-- Name: offering_cpu_configurations offering_cpu_configurations_pkey; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.offering_cpu_configurations
    ADD CONSTRAINT offering_cpu_configurations_pkey PRIMARY KEY (id);


--
-- Name: offering_gpu_configurations offering_gpu_configurations_pkey; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.offering_gpu_configurations
    ADD CONSTRAINT offering_gpu_configurations_pkey PRIMARY KEY (id);


--
-- Name: price_alerts price_alerts_pkey; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.price_alerts
    ADD CONSTRAINT price_alerts_pkey PRIMARY KEY (id);


--
-- Name: price_observations price_observations_pkey; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.price_observations
    ADD CONSTRAINT price_observations_pkey PRIMARY KEY (id);


--
-- Name: pricing_plans pricing_plans_pkey; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.pricing_plans
    ADD CONSTRAINT pricing_plans_pkey PRIMARY KEY (id);


--
-- Name: provider_regions provider_regions_pkey; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.provider_regions
    ADD CONSTRAINT provider_regions_pkey PRIMARY KEY (id);


--
-- Name: providers providers_pkey; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.providers
    ADD CONSTRAINT providers_pkey PRIMARY KEY (id);


--
-- Name: schedule_configs schedule_configs_pkey; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.schedule_configs
    ADD CONSTRAINT schedule_configs_pkey PRIMARY KEY (id);


--
-- Name: source_attributions source_attributions_pkey; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.source_attributions
    ADD CONSTRAINT source_attributions_pkey PRIMARY KEY (id);


--
-- Name: storage_providers storage_providers_pkey; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.storage_providers
    ADD CONSTRAINT storage_providers_pkey PRIMARY KEY (id);


--
-- Name: storage_tiers storage_tiers_pkey; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.storage_tiers
    ADD CONSTRAINT storage_tiers_pkey PRIMARY KEY (id);


--
-- Name: tbl_fin_mkt_hist tbl_fin_mkt_hist_pkey; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.tbl_fin_mkt_hist
    ADD CONSTRAINT tbl_fin_mkt_hist_pkey PRIMARY KEY (id);


--
-- Name: tbl_gpu_prc_hist tbl_gpu_prc_hist_pkey; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.tbl_gpu_prc_hist
    ADD CONSTRAINT tbl_gpu_prc_hist_pkey PRIMARY KEY (id);


--
-- Name: tbl_news_arti tbl_news_arti_pkey; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.tbl_news_arti
    ADD CONSTRAINT tbl_news_arti_pkey PRIMARY KEY (id);


--
-- Name: tbl_obx_evt tbl_obx_evt_pkey; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.tbl_obx_evt
    ADD CONSTRAINT tbl_obx_evt_pkey PRIMARY KEY (id);


--
-- Name: tbl_rtl_prc_hist tbl_rtl_prc_hist_pkey; Type: CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.tbl_rtl_prc_hist
    ADD CONSTRAINT tbl_rtl_prc_hist_pkey PRIMARY KEY (id);


--
-- Name: idx_fin_mkt_sym_ts; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX idx_fin_mkt_sym_ts ON public.tbl_fin_mkt_hist USING btree (sym_cd, ts);


--
-- Name: idx_gpu_prc_mdl_ts; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX idx_gpu_prc_mdl_ts ON public.tbl_gpu_prc_hist USING btree (gpu_mdl, ts);


--
-- Name: idx_gpu_prc_prv_ts; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX idx_gpu_prc_prv_ts ON public.tbl_gpu_prc_hist USING btree (prv_id, ts);


--
-- Name: idx_news_arti_pub_src; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX idx_news_arti_pub_src ON public.tbl_news_arti USING btree (pub_ts, src_nm);


--
-- Name: idx_rtl_prc_hw_mdl_ts; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX idx_rtl_prc_hw_mdl_ts ON public.tbl_rtl_prc_hist USING btree (hw_typ, mdl_nm, ts);


--
-- Name: idx_rtl_prc_pltf_mdl_ts; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX idx_rtl_prc_pltf_mdl_ts ON public.tbl_rtl_prc_hist USING btree (pltf_nm, mdl_nm, ts);


--
-- Name: ix_collection_runs_provider_id; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_collection_runs_provider_id ON public.collection_runs USING btree (provider_id);


--
-- Name: ix_collection_runs_provider_started; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_collection_runs_provider_started ON public.collection_runs USING btree (provider_id, started_at);


--
-- Name: ix_cpu_models_manufacturer_id; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_cpu_models_manufacturer_id ON public.cpu_models USING btree (manufacturer_id);


--
-- Name: ix_cpu_variants_model_id; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_cpu_variants_model_id ON public.cpu_variants USING btree (model_id);


--
-- Name: ix_data_quality_issues_observation_id; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_data_quality_issues_observation_id ON public.data_quality_issues USING btree (observation_id);


--
-- Name: ix_data_quality_issues_run_id; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_data_quality_issues_run_id ON public.data_quality_issues USING btree (run_id);


--
-- Name: ix_gpu_models_manufacturer_id; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_gpu_models_manufacturer_id ON public.gpu_models USING btree (manufacturer_id);


--
-- Name: ix_gpu_variants_model_id; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_gpu_variants_model_id ON public.gpu_variants USING btree (model_id);


--
-- Name: ix_idempotency_keys_key; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE UNIQUE INDEX ix_idempotency_keys_key ON public.idempotency_keys USING btree (key);


--
-- Name: ix_instance_offerings_machine_type_name; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_instance_offerings_machine_type_name ON public.instance_offerings USING btree (machine_type_name);


--
-- Name: ix_instance_offerings_provider_id; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_instance_offerings_provider_id ON public.instance_offerings USING btree (provider_id);


--
-- Name: ix_instance_offerings_region_id; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_instance_offerings_region_id ON public.instance_offerings USING btree (region_id);


--
-- Name: ix_memory_manufacturers_name; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE UNIQUE INDEX ix_memory_manufacturers_name ON public.memory_manufacturers USING btree (name);


--
-- Name: ix_memory_modules_manufacturer_id; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_memory_modules_manufacturer_id ON public.memory_modules USING btree (manufacturer_id);


--
-- Name: ix_offering_cpu_configurations_cpu_variant_id; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_offering_cpu_configurations_cpu_variant_id ON public.offering_cpu_configurations USING btree (cpu_variant_id);


--
-- Name: ix_offering_cpu_configurations_offering_id; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_offering_cpu_configurations_offering_id ON public.offering_cpu_configurations USING btree (offering_id);


--
-- Name: ix_offering_gpu_configurations_gpu_variant_id; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_offering_gpu_configurations_gpu_variant_id ON public.offering_gpu_configurations USING btree (gpu_variant_id);


--
-- Name: ix_offering_gpu_configurations_offering_id; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_offering_gpu_configurations_offering_id ON public.offering_gpu_configurations USING btree (offering_id);


--
-- Name: ix_price_alerts_gpu_model_id; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_price_alerts_gpu_model_id ON public.price_alerts USING btree (gpu_model_id);


--
-- Name: ix_price_alerts_user_email; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_price_alerts_user_email ON public.price_alerts USING btree (user_email);


--
-- Name: ix_price_observations_pricing_plan_id; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_price_observations_pricing_plan_id ON public.price_observations USING btree (pricing_plan_id);


--
-- Name: ix_pricing_plans_offering_id; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_pricing_plans_offering_id ON public.pricing_plans USING btree (offering_id);


--
-- Name: ix_provider_regions_provider_id; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_provider_regions_provider_id ON public.provider_regions USING btree (provider_id);


--
-- Name: ix_provider_regions_provider_region_id; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_provider_regions_provider_region_id ON public.provider_regions USING btree (provider_region_id);


--
-- Name: ix_providers_name; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE UNIQUE INDEX ix_providers_name ON public.providers USING btree (name);


--
-- Name: ix_providers_slug; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE UNIQUE INDEX ix_providers_slug ON public.providers USING btree (slug);


--
-- Name: ix_schedule_configs_provider_id; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_schedule_configs_provider_id ON public.schedule_configs USING btree (provider_id);


--
-- Name: ix_source_attributions_provider_id; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_source_attributions_provider_id ON public.source_attributions USING btree (provider_id);


--
-- Name: ix_storage_providers_name; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE UNIQUE INDEX ix_storage_providers_name ON public.storage_providers USING btree (name);


--
-- Name: ix_storage_tiers_provider_id; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_storage_tiers_provider_id ON public.storage_tiers USING btree (provider_id);


--
-- Name: ix_tbl_fin_mkt_hist_ast_typ; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_tbl_fin_mkt_hist_ast_typ ON public.tbl_fin_mkt_hist USING btree (ast_typ);


--
-- Name: ix_tbl_fin_mkt_hist_sym_cd; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_tbl_fin_mkt_hist_sym_cd ON public.tbl_fin_mkt_hist USING btree (sym_cd);


--
-- Name: ix_tbl_fin_mkt_hist_ts; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_tbl_fin_mkt_hist_ts ON public.tbl_fin_mkt_hist USING btree (ts);


--
-- Name: ix_tbl_gpu_prc_hist_cpu_mdl; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_tbl_gpu_prc_hist_cpu_mdl ON public.tbl_gpu_prc_hist USING btree (cpu_mdl);


--
-- Name: ix_tbl_gpu_prc_hist_gpu_mdl; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_tbl_gpu_prc_hist_gpu_mdl ON public.tbl_gpu_prc_hist USING btree (gpu_mdl);


--
-- Name: ix_tbl_gpu_prc_hist_prv_id; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_tbl_gpu_prc_hist_prv_id ON public.tbl_gpu_prc_hist USING btree (prv_id);


--
-- Name: ix_tbl_gpu_prc_hist_ts; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_tbl_gpu_prc_hist_ts ON public.tbl_gpu_prc_hist USING btree (ts);


--
-- Name: ix_tbl_news_arti_arti_url; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE UNIQUE INDEX ix_tbl_news_arti_arti_url ON public.tbl_news_arti USING btree (arti_url);


--
-- Name: ix_tbl_news_arti_crt_ts; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_tbl_news_arti_crt_ts ON public.tbl_news_arti USING btree (crt_ts);


--
-- Name: ix_tbl_news_arti_pub_ts; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_tbl_news_arti_pub_ts ON public.tbl_news_arti USING btree (pub_ts);


--
-- Name: ix_tbl_news_arti_src_nm; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_tbl_news_arti_src_nm ON public.tbl_news_arti USING btree (src_nm);


--
-- Name: ix_tbl_obx_evt_proc_st; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_tbl_obx_evt_proc_st ON public.tbl_obx_evt USING btree (proc_st);


--
-- Name: ix_tbl_obx_evt_tpc_nm; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_tbl_obx_evt_tpc_nm ON public.tbl_obx_evt USING btree (tpc_nm);


--
-- Name: ix_tbl_rtl_prc_hist_mdl_nm; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_tbl_rtl_prc_hist_mdl_nm ON public.tbl_rtl_prc_hist USING btree (mdl_nm);


--
-- Name: ix_tbl_rtl_prc_hist_pltf_nm; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_tbl_rtl_prc_hist_pltf_nm ON public.tbl_rtl_prc_hist USING btree (pltf_nm);


--
-- Name: ix_tbl_rtl_prc_hist_ts; Type: INDEX; Schema: public; Owner: infraindex
--

CREATE INDEX ix_tbl_rtl_prc_hist_ts ON public.tbl_rtl_prc_hist USING btree (ts);


--
-- Name: SYS_CD_BAS SYS_CD_BAS_SYS_GROUP_ID_fkey; Type: FK CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public."SYS_CD_BAS"
    ADD CONSTRAINT "SYS_CD_BAS_SYS_GROUP_ID_fkey" FOREIGN KEY ("SYS_GROUP_ID") REFERENCES public."SYS_CD_GROUP_BAS"("SYS_GROUP_ID");


--
-- Name: cpu_models cpu_models_manufacturer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.cpu_models
    ADD CONSTRAINT cpu_models_manufacturer_id_fkey FOREIGN KEY (manufacturer_id) REFERENCES public.cpu_manufacturers(id);


--
-- Name: cpu_variants cpu_variants_model_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.cpu_variants
    ADD CONSTRAINT cpu_variants_model_id_fkey FOREIGN KEY (model_id) REFERENCES public.cpu_models(id);


--
-- Name: gpu_models gpu_models_manufacturer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.gpu_models
    ADD CONSTRAINT gpu_models_manufacturer_id_fkey FOREIGN KEY (manufacturer_id) REFERENCES public.gpu_manufacturers(id);


--
-- Name: gpu_variants gpu_variants_model_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.gpu_variants
    ADD CONSTRAINT gpu_variants_model_id_fkey FOREIGN KEY (model_id) REFERENCES public.gpu_models(id);


--
-- Name: instance_offerings instance_offerings_provider_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.instance_offerings
    ADD CONSTRAINT instance_offerings_provider_id_fkey FOREIGN KEY (provider_id) REFERENCES public.providers(id);


--
-- Name: instance_offerings instance_offerings_region_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.instance_offerings
    ADD CONSTRAINT instance_offerings_region_id_fkey FOREIGN KEY (region_id) REFERENCES public.provider_regions(id);


--
-- Name: memory_modules memory_modules_manufacturer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.memory_modules
    ADD CONSTRAINT memory_modules_manufacturer_id_fkey FOREIGN KEY (manufacturer_id) REFERENCES public.memory_manufacturers(id);


--
-- Name: offering_cpu_configurations offering_cpu_configurations_cpu_variant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.offering_cpu_configurations
    ADD CONSTRAINT offering_cpu_configurations_cpu_variant_id_fkey FOREIGN KEY (cpu_variant_id) REFERENCES public.cpu_variants(id);


--
-- Name: offering_cpu_configurations offering_cpu_configurations_offering_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.offering_cpu_configurations
    ADD CONSTRAINT offering_cpu_configurations_offering_id_fkey FOREIGN KEY (offering_id) REFERENCES public.instance_offerings(id);


--
-- Name: offering_gpu_configurations offering_gpu_configurations_gpu_variant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.offering_gpu_configurations
    ADD CONSTRAINT offering_gpu_configurations_gpu_variant_id_fkey FOREIGN KEY (gpu_variant_id) REFERENCES public.gpu_variants(id);


--
-- Name: offering_gpu_configurations offering_gpu_configurations_offering_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.offering_gpu_configurations
    ADD CONSTRAINT offering_gpu_configurations_offering_id_fkey FOREIGN KEY (offering_id) REFERENCES public.instance_offerings(id);


--
-- Name: price_alerts price_alerts_gpu_model_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.price_alerts
    ADD CONSTRAINT price_alerts_gpu_model_id_fkey FOREIGN KEY (gpu_model_id) REFERENCES public.gpu_models(id);


--
-- Name: price_observations price_observations_pricing_plan_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.price_observations
    ADD CONSTRAINT price_observations_pricing_plan_id_fkey FOREIGN KEY (pricing_plan_id) REFERENCES public.pricing_plans(id);


--
-- Name: pricing_plans pricing_plans_offering_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.pricing_plans
    ADD CONSTRAINT pricing_plans_offering_id_fkey FOREIGN KEY (offering_id) REFERENCES public.instance_offerings(id);


--
-- Name: provider_regions provider_regions_provider_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.provider_regions
    ADD CONSTRAINT provider_regions_provider_id_fkey FOREIGN KEY (provider_id) REFERENCES public.providers(id);


--
-- Name: source_attributions source_attributions_license_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.source_attributions
    ADD CONSTRAINT source_attributions_license_id_fkey FOREIGN KEY (license_id) REFERENCES public.data_licenses(id);


--
-- Name: storage_tiers storage_tiers_provider_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: infraindex
--

ALTER TABLE ONLY public.storage_tiers
    ADD CONSTRAINT storage_tiers_provider_id_fkey FOREIGN KEY (provider_id) REFERENCES public.storage_providers(id);


--
-- PostgreSQL database dump complete
--

\unrestrict Gpr1CzDpQNBgaIOiOQBTAgXfnuQ5NGmVh99qYpHetthyQxXvcOCRP4eYhudlOpQ

