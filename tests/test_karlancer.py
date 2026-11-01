import httpx
import pytest
from conftest import fixture

pytestmark = pytest.mark.anyio

P = "/api/publics"
TOOLS = {
    "kl_projects",
    "kl_project",
    "kl_skills",
    "kl_categories",
    "kl_freelancers",
    "kl_top_freelancers",
    "kl_freelancer",
    "kl_services",
    "kl_service",
    "kl_worksamples",
    "kl_worksample",
    "kl_similar_projects",
    "kl_market_rate",
    "kl_trending_skills",
}


async def test_all_tools_are_read_only_and_described(client):
    tools = (await client.list_tools()).tools
    assert {t.name for t in tools} == TOOLS
    for t in tools:
        assert t.annotations.read_only_hint is True, t.name
        assert t.title and t.description.splitlines()[0].endswith("."), t.name
        assert all("title" not in prop for prop in t.input_schema.get("properties", {}).values()), t.name


async def test_calls_send_the_headers_of_the_sites_axios_xhr(client, api):
    api[P + "/search/projects"] = fixture("projects.json")
    await client.call_tool("kl_projects", {"query": "python"})
    h = api.calls[0].headers  # same-origin axios call: no Origin, origin-only Referer
    assert (h["accept"], h["referer"], h["sec-fetch-site"], h["sec-fetch-mode"], h["sec-fetch-dest"]) == (
        "application/json, text/plain, */*",
        "https://www.karlancer.com/",
        "same-origin",
        "cors",
        "empty",
    )
    assert h["priority"] == "u=1, i" and "origin" not in h and h["accept-language"].startswith("fa-IR")


async def test_projects_sends_site_params_and_trims(client, api):
    api[P + "/search/projects"] = fixture("projects.json")
    r = (
        await client.call_tool(
            "kl_projects",
            {"query": "python", "skills": [9923, 1369], "min_budget": 1000000, "urgent": True, "page": 2},
        )
    ).structured_content
    q = api.calls[0].url.params
    assert q["q"] == "python" and q["skillIds[0]"] == "9923" and q["skillIds[1]"] == "1369"
    assert q["price[min]"] == "1000000" and q["is_urgent"] == "1" and q["page"] == "2" and q["order"] == "newest"
    assert "price[max]" not in q and "low_competition" not in q
    first = r["results"][0]
    assert r["total"] > 0 and len(r["results"]) == 2 and r["pages"] >= 1
    assert len(first["token"]) == 12 and first["url"].startswith("https://www.karlancer.com/projects/")
    assert first["budget_toman"]["min"] <= first["budget_toman"]["max"] and first["skills"]
    assert len(first["description"]) <= 300


async def test_project_accepts_token_slug_or_url(client, api):
    api[P + "/projects/e781r5me46o1"] = fixture("project.json")
    for ref in (
        "e781r5me46o1",
        "نیازمند-فردی-برای-آموزش-کارگاه-e781r5me46o1",
        "https://www.karlancer.com/projects/%D9%86%D9%8A%D8%A7-e781r5me46o1?x=1",
    ):
        r = (await client.call_tool("kl_project", {"project": ref})).structured_content
        assert r["token"] == "e781r5me46o1" and r["category_path"] and r["hire_deadline"]
        assert r["skills"][0].keys() == {"id", "name"}


async def test_api_error_message_is_passed_on(client, api):
    api[P + "/projects/zzz"] = lambda req: httpx.Response(
        404, json={"status": "failed", "data": None, "error": "پروژه یافت نشد"}
    )
    r = await client.call_tool("kl_project", {"project": "zzz"})
    assert r.is_error and "404" in r.content[0].text and "پروژه یافت نشد" in r.content[0].text


async def test_skills_and_categories(client, api):
    api[P + "/skills/auto-complete"] = fixture("skills_ac.json")
    api[P + "/skills"] = fixture("skills.json")
    api[P + "/lists/provinces"] = fixture("provinces.json")
    s = (await client.call_tool("kl_skills", {"query": "python"})).structured_content
    assert s["skills"][0] == {"id": 9923, "name": "python", "uses": s["skills"][0]["uses"]}
    assert api.calls[0].url.params["s"] == "python"
    c = (await client.call_tool("kl_categories", {})).structured_content
    ids = {x["id"] for x in c["categories"]}
    assert {2, 6} <= ids and len(c["provinces"]) == 3
    assert all(x["name"] != "صفحات مادر" for x in c["categories"])  # group without a category id


async def test_freelancers_and_top(client, api):
    api[P + "/search/freelancers"] = fixture("freelancers.json")
    api[P + "/lists/top-freelancers"] = fixture("top_freelancers.json")
    r = (
        await client.call_tool(
            "kl_freelancers", {"query": "python", "skills": [9923], "province": "اصفهان", "active_recently": True}
        )
    ).structured_content
    q = api.calls[0].url.params
    assert q["province"] == "اصفهان" and q["last_visit"] == "true" and q["skillIds[0]"] == "9923"
    f = r["results"][0]
    assert f["url"] == f"https://www.karlancer.com/profile/{f['id']}" and f["skills"] and f["username"]
    t = (await client.call_tool("kl_top_freelancers", {})).structured_content
    assert len(t["results"]) == 2 and t["results"][0]["stars"] > 4


async def test_freelancer_profile_and_reviews(client, api):
    api[P + "/new-profile/1408809"] = fixture("profile.json")
    r = (await client.call_tool("kl_freelancer", {"id": 1408809, "review_page": 2})).structured_content
    assert api.calls[0].url.params["page"] == "2"
    assert r["username"] and r["skills"] and r["experience"] and r["completed_projects"] > 0
    rv = r["recent_reviews"][0]
    assert rv["stars"] and rv["project"] and rv["date"].startswith("20")


async def test_services_and_detail(client, api):
    api[P + "/search/services"] = fixture("services.json")
    api[P + "/new-services/n923oon6r2wm"] = fixture("service.json")
    r = (
        await client.call_tool("kl_services", {"query": "logo", "max_price": 500000, "featured": True})
    ).structured_content
    q = api.calls[0].url.params
    assert q["price[max]"] == "500000" and q["feature"] == "1" and q["order"] == "relevant"
    s = r["results"][0]
    assert len(s["token"]) == 12 and s["price_toman"] and s["seller"]["username"]
    d = (await client.call_tool("kl_service", {"service": "n923oon6r2wm"})).structured_content
    assert d["price_toman"] and d["seller"]["username"] and d["skills"] and d["requirements"]


async def test_empty_503_is_retried(client, api):
    answers = iter([httpx.Response(503), httpx.Response(200, json=fixture("top_freelancers.json"))])
    api[P + "/lists/top-freelancers"] = lambda req: next(answers)
    r = (await client.call_tool("kl_top_freelancers", {})).structured_content
    assert len(r["results"]) == 2 and len(api.calls) == 2


async def test_cache_serves_second_call(client, api):
    api[P + "/lists/top-freelancers"] = fixture("top_freelancers.json")
    await client.call_tool("kl_top_freelancers", {})
    await client.call_tool("kl_top_freelancers", {})
    assert len(api.calls) == 1


async def test_service_detail_adds_packages_and_reviews(client, api):
    api[P + "/new-services/n923oon6r2wm"] = fixture("service.json")
    api[P + "/service-rest/41682"] = fixture("service_rest.json")
    d = (await client.call_tool("kl_service", {"service": "n923oon6r2wm"})).structured_content
    assert d["packages"][0]["price_toman"] > 0 and d["buyer_reviews"][0]["stars"]


async def test_service_detail_survives_missing_reviews(client, api):
    api[P + "/new-services/n923oon6r2wm"] = fixture("service.json")  # service-rest answers 404
    d = (await client.call_tool("kl_service", {"service": "n923oon6r2wm"})).structured_content
    assert d["price_toman"] and d["buyer_reviews"] == []


async def test_worksamples_search_and_by_freelancer(client, api):
    api[P + "/search/worksamples"] = fixture("worksamples.json")
    api[P + "/worksamples/user/1408809"] = fixture("worksamples_user.json")
    r = (
        await client.call_tool("kl_worksamples", {"query": "logo", "skills": [14], "order": "newest"})
    ).structured_content
    q = api.calls[0].url.params
    assert q["q"] == "logo" and q["skillIds[0]"] == "14" and q["order"] == "newest"
    w = r["results"][0]
    assert (
        r["total"] > 0
        and len(w["token"]) == 12
        and w["skills"]
        and w["url"].startswith("https://www.karlancer.com/worksample/")
    )
    u = (await client.call_tool("kl_worksamples", {"freelancer_id": 1408809})).structured_content
    assert len(u["results"]) == 1 and u["results"][0]["freelancer"]["id"] == 1408809


async def test_worksample_detail_with_similar(client, api):
    api[P + "/new-worksample/e049mo32084r"] = fixture("worksample.json")
    api[P + "/similar-worksamples/721255"] = fixture("worksample_similar.json")
    r = (await client.call_tool("kl_worksample", {"worksample": "e049mo32084r"})).structured_content
    assert r["owner"]["username"] and r["budget_toman"]["max"] and len(r["similar"]) == 2


async def test_similar_projects(client, api):
    api[P + "/suggest/project/m080rr13784r"] = fixture("suggest.json")
    r = (await client.call_tool("kl_similar_projects", {"project": "m080rr13784r"})).structured_content
    assert len(r["results"]) == 3 and len(r["results"][0]["token"]) == 12


async def test_market_rate_and_trending_are_computed_from_samples(client, api):
    api[P + "/search/projects"] = fixture("projects.json")
    api[P + "/search/services"] = fixture("services.json")
    api[P + "/search/freelancers"] = fixture("freelancers.json")
    m = (await client.call_tool("kl_market_rate", {"skill": 9923, "sample_pages": 1})).structured_content
    spread = m["project_budget_toman"]
    assert spread["low"] <= spread["median"] <= spread["high"] and m["projects_sampled"] == 2
    assert m["service_price_toman"]["median"] > 0 and m["freelancers_with_skill"] > 0
    bad = await client.call_tool("kl_market_rate", {})
    assert bad.is_error
    t = (await client.call_tool("kl_trending_skills", {"pages": 1, "top": 3})).structured_content
    assert t["projects_sampled"] == 2 and t["skills"][0]["projects"] >= t["skills"][-1]["projects"]
