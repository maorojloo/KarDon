import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String ,ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

engine = create_engine("sqlite:///kardon.db", echo=True)


class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True)
    url = Column(String)

    def __repr__(self):
        return "<User(id='%s', url='%s')>" % (
            self.id,
            self.url,
        )
        
        
class JobDetail(Base):
    __tablename__ = "JobsDetail"
    
    user_id = Column(Integer, ForeignKey('jobs.id'), primary_key=True)
    url = Column(String, ForeignKey('jobs.url'))
    title = Column(String)
    description= Column(String)
    companynametitleFa= Column(String)
    companylogo = Column(String)
    locations = Column(String)
    workTypes = Column(String)
    hasWorkExperienceRequirement = Column(String)
    hasAlternativeMilitary = Column(String)
    benefits = Column(String)
    publishTimedate = Column(String)
    jobBoardorganizationColor = Column(String)
    jobBoardtitleFa = Column(String)
    jobBoardtitleEn = Column(String)
    companyDetailsSummarynametitleFa = Column(String)   
    seniorityLevel= Column(String)  

    def __repr__(self):
        return "<User(id='%s', url='%s')>" % (
            self.id,
            self.title,
        )
        
        
        
        
Base.metadata.create_all(engine)