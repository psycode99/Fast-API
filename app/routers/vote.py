from fastapi import status, Depends, HTTPException, APIRouter
from ..schemas import Vote
from ..database import get_db
from .. import oauth2, models
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/votes',
    tags=['Votes']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_vote(vote: Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user )):
    print(vote.dir)
    found_vote = db.query(models.Vote).filter_by(post_id=vote.post_id, user_id=current_user.id).first()
    
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id) 
        db.add(new_vote)
        db.commit()
        return {"Message":"Successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Vote not found")
        db.delete(found_vote)
        db.commit()
        return {"Message":"Successfully deleted vote"}