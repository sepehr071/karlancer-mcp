import pytest

pytestmark = [pytest.mark.live, pytest.mark.anyio]


async def test_live_skill_then_projects(client):
    s = (await client.call_tool("kl_skills", {"query": "python"})).structured_content
    py = next(x for x in s["skills"] if x["name"] == "python")
    r = (await client.call_tool("kl_projects", {"skills": [py["id"]], "min_budget": 1000000})).structured_content
    assert r["total"] > 0 and len(r["results"]) > 0
    assert all("python" in [k.lower() for k in p["skills"]] for p in r["results"])
    assert all(p["budget_toman"]["max"] >= 1000000 for p in r["results"])


async def test_live_project_detail(client):
    first = (await client.call_tool("kl_projects", {"order": "newest"})).structured_content["results"][0]
    d = (await client.call_tool("kl_project", {"project": first["token"]})).structured_content
    assert d["title"] == first["title"] and d["category_path"] and d["description"]


async def test_live_budget_order(client):
    r = (await client.call_tool("kl_projects", {"order": "max-budget"})).structured_content["results"]
    top = [p["budget_toman"]["max"] for p in r]
    assert top == sorted(top, reverse=True)


async def test_live_categories(client):
    c = (await client.call_tool("kl_categories", {})).structured_content
    assert {2, 6} <= {x["id"] for x in c["categories"]} and "تهران" in c["provinces"]


async def test_live_freelancer_flow(client):
    f = (await client.call_tool("kl_freelancers", {"query": "python", "province": "تهران"})).structured_content
    assert f["total"] > 0
    p = (await client.call_tool("kl_freelancer", {"id": f["results"][0]["id"]})).structured_content
    assert p["username"] == f["results"][0]["username"]


async def test_live_top_freelancers(client):
    t = (await client.call_tool("kl_top_freelancers", {})).structured_content
    assert len(t["results"]) > 3


async def test_live_service_flow(client):
    r = (await client.call_tool("kl_services", {"query": "logo"})).structured_content
    d = (await client.call_tool("kl_service", {"service": r["results"][0]["token"]})).structured_content
    assert d["title"] == r["results"][0]["title"] and d["price_toman"] > 0


async def test_live_worksamples_and_detail(client):
    r = (await client.call_tool("kl_worksamples", {"query": "logo"})).structured_content
    assert r["total"] > 0
    d = (await client.call_tool("kl_worksample", {"worksample": r["results"][0]["token"]})).structured_content
    assert d["title"] == r["results"][0]["title"] and d["owner"]["username"]
    mine = (await client.call_tool("kl_worksamples", {"freelancer_id": d["freelancer"]["id"]})).structured_content
    assert mine["results"]


async def test_live_market_trending_similar_and_service_reviews(client):
    m = (await client.call_tool("kl_market_rate", {"query": "python", "sample_pages": 1})).structured_content
    assert m["project_budget_toman"]["median"] > 0 and m["open_projects"] > 0
    t = (await client.call_tool("kl_trending_skills", {"pages": 1})).structured_content
    assert t["skills"] and t["skills"][0]["id"]
    p = (await client.call_tool("kl_projects", {"order": "newest"})).structured_content["results"][0]
    s = (await client.call_tool("kl_similar_projects", {"project": p["token"]})).structured_content
    assert "results" in s
    sv = (await client.call_tool("kl_services", {"query": "logo"})).structured_content["results"][0]
    d = (await client.call_tool("kl_service", {"service": sv["token"]})).structured_content
    assert d["packages"]
