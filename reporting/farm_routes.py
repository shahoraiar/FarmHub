from fastapi import APIRouter, Depends, HTTPException, Header
from django.contrib.auth import get_user_model
from .models import Farm, Farmer, Cow, CowActivity, MilkProduction
from .user_routes import get_current_user
from sqlalchemy import func, extract


User = get_user_model()
router = APIRouter(prefix="", tags=["Farms"])
from .database import SessionLocal

@router.get("/farms")
def get_farms(current_user=Depends(get_current_user)):
    db = SessionLocal()
    try:
        if current_user.is_superuser:
            farms = db.query(Farm).all()
        elif current_user.groups.filter(name="SuperAdmin").exists():
            agents = User.objects.filter(created_by=current_user.id)
            farms = db.query(Farm).filter(
                (Farm.created_by_id == current_user.id) | 
                (Farm.created_by_id.in_([a.id for a in agents]))
            ).all()
        elif current_user.groups.filter(name="Agent").exists():
            farms = db.query(Farm).filter(Farm.agent_id == current_user.id).all()
        elif current_user.groups.filter(name="Farmer").exists():
            farmer = db.query(Farmer).filter(Farmer.user_id == current_user.id).first()
            farms = []
            if farmer and farmer.farm_id:
                farms = db.query(Farm).filter(Farm.id == farmer.farm_id).all()
        else:
            farms = []

        farm_list = []
        for farm in farms:
            farm_list.append({
                "id": farm.id,
                "name": farm.name,
                "location": farm.location,
                "agent_id": farm.agent_id,
                "created_by": farm.created_by_id,
            })

        return{
            "total": len(farm_list),
            "farms": farm_list
        }
    finally:
        db.close()


@router.get("/cow/details")
def get_cows(current_user=Depends(get_current_user)):
    db = SessionLocal()
    try:
        if current_user.is_superuser:
            cows = db.query(Cow).all()

        elif current_user.groups.filter(name="SuperAdmin").exists():
            agents = User.objects.filter(created_by=current_user.id)
            print('agents : ', agents)
            agent_ids = [agent.id for agent in agents]
            print('agents id : ', agent_ids)

            farmers = db.query(Farmer).filter(Farmer.created_by_id.in_(agent_ids)).all()
            farmer_ids = [farmer.id for farmer in farmers]

            cows = db.query(Cow).filter(Cow.farmer_id.in_(farmer_ids)).all()
        elif current_user.groups.filter(name="Agent").exists():
            farms = db.query(Farm).filter(Farm.agent_id == current_user.id).all()
            farm_ids = [f.id for f in farms]
            cows = db.query(Cow).filter(Cow.farm_id.in_(farm_ids)).all()
        elif current_user.groups.filter(name="Farmer").exists():
            farmer = db.query(Farmer).filter(Farmer.user_id == current_user.id).first()
            if farmer:
                cows = db.query(Cow).filter(Cow.farmer_id == farmer.id).all()
            else:
                cows = []
        else:
            cows = []

        cow_list = []

        for cow in cows:
            cow_list.append({
                "id": cow.id,
                "cow_tag": cow.cow_tag,
                "name": cow.name,
                "breed": cow.breed,
                "gender": cow.gender,
                "farm_id": cow.farm_id,
                "farmer_id": cow.farmer_id,
                "weight_kg": cow.weight_kg,
                "color": cow.color,
                "is_sold": cow.is_sold,
            })

        return {
            "total cow": len(cow_list),
            "cows": cow_list
        }
    finally:
        db.close()

@router.get("/cow/activity/summary")
def cow_summary(current_user=Depends(get_current_user)):
    db = SessionLocal()
    try:
        cows_query = db.query(Cow)
        
        if current_user.is_superuser:
            cows = cows_query.all()
        elif current_user.groups.filter(name="SuperAdmin").exists():
            agents = db.query(Farmer).filter(Farmer.user_id.in_(
                [u.id for u in User.objects.filter(created_by=current_user.id)]
            )).all()
            agent_ids = [a.id for a in agents]
            cows = cows_query.filter(
                (Cow.farmer_id.in_(agent_ids)) |
                (Cow.farmer_id == current_user.id)
            ).all()
        elif current_user.groups.filter(name="Agent").exists():
            print('current user id : ', current_user.id) 
            farmers = db.query(Farmer).filter(Farmer.created_by_id  == current_user.id).all()
            print('farmers : ', farmers)
            farmer_ids = [f.id for f in farmers]
            cows = cows_query.filter(Cow.farmer_id.in_(farmer_ids)).all()
        elif current_user.groups.filter(name="Farmer").exists():
            farmer = db.query(Farmer).filter(Farmer.user_id == current_user.id).first()
            cows = []
            if farmer:
                cows = cows_query.filter(Cow.farmer_id == farmer.id).all()
        else:
            cows = []

        cow_data = []
        grand_total = 0

        for cow in cows:
            activity_info = db.query(
                func.count(CowActivity.id),
                func.coalesce(func.sum(CowActivity.cost), 0)
            ).filter(CowActivity.cow_id == cow.id).first()

            treatment_count = activity_info[0]
            total_cost = float(activity_info[1] or 0)
            grand_total += total_cost

            cow_data.append({
                "cow_tag": cow.cow_tag,
                "cow_name": cow.name,
                "treatment_count": treatment_count,
                "total_cost": total_cost
            })

        return {
            "cows": cow_data,
            "grand_total_cost": grand_total
        }

    finally:
        db.close()

@router.get("/production/milk/summary")
def milk_summary(current_user=Depends(get_current_user)):
    db = SessionLocal()
    try:
        cow_query = db.query(Cow)
        cows = []

        if current_user.is_superuser:
            cows = cow_query.all()
        elif current_user.groups.filter(name="SuperAdmin").exists():
            all_agents = User.objects.filter(created_by=current_user.id)
            agent_ids = [agent.id for agent in all_agents]
            cows = cow_query.filter(
                (Cow.farmer_id.in_(agent_ids)) |
                (Cow.farmer_id == current_user.id)
            ).all()
        elif current_user.groups.filter(name="Agent").exists():
            linked_farmers = db.query(Farmer).filter(Farmer.created_by_id == current_user.id).all()
            farmer_ids = [farmer.id for farmer in linked_farmers]
            cows = cow_query.filter(Cow.farmer_id.in_(farmer_ids)).all()
        elif current_user.groups.filter(name="Farmer").exists():
            farmer = db.query(Farmer).filter(Farmer.user_id == current_user.id).first()
            if farmer:
                cows = cow_query.filter(Cow.farmer_id == farmer.id).all()

        milk_summary_list = []
        total_milk_all_cows = 0

        for cow in cows:
            milk_info = db.query(
                func.count(MilkProduction.id),  
                func.coalesce(func.sum(MilkProduction.total_yield_liters), 0)  
            ).filter(MilkProduction.cow_id == cow.id).first()

            milk_count = milk_info[0] or 0
            total_milk_cow = float(milk_info[1] or 0)
            total_milk_all_cows += total_milk_cow

            monthwise_milk = []
            month_query = db.query(
                extract('year', MilkProduction.date).label("year"),
                extract('month', MilkProduction.date).label("month"),
                func.coalesce(func.sum(MilkProduction.total_yield_liters), 0).label("monthly_total")
            ).filter(MilkProduction.cow_id == cow.id).group_by("year", "month").order_by("year", "month").all()

            for record in month_query:
                monthwise_milk.append({
                    "year": int(record.year),
                    "month": int(record.month),
                    "total_liters": float(record.monthly_total or 0)
                })

            milk_summary_list.append({
                "cow_tag": cow.cow_tag,
                "cow_name": cow.name,
                "milk_times_recorded": milk_count,
                "total_milk": total_milk_cow,
                "monthwise_milk": monthwise_milk
            })

        return {
            "milk_summary": milk_summary_list,
            "grand_total_milk": total_milk_all_cows
        }

    finally:
        db.close()


