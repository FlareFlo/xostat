import React from "react";
import { Col, Card, Row, Container } from "react-bootstrap";

const MinMaxAvg = () => {
  const totals = 9999;
  const min = 9999;
  const max = 9999;
  const avg = 9999;
  const kills = 9999;
  const assists = 9999;
  const deaths = 9999;
  const damage = 9999;
  const damageReceived = 9999;
  const mvp = 9999;
  const score = 9999;
  const time = 9999;

  return (
    <Col className="d-flex">
      <Card className="flex-fill">
        <Card.Body className="py-4">
          <Container>
            <Row>
              <Col>
                <div className="row d-flex justify-content-center">
                  <div className="flex-grow-1 justify-content-center">
                    <h3 className="mb-2">Totals</h3>
                    <p className="mb-2">{totals}</p>
                  </div>
                </div>
              </Col>
              <Col>
                <div className="row d-flex justify-content-center">
                  <div className="flex-grow-1 justify-content-center">
                    <h3 className="mb-2">Min</h3>
                    <p className="mb-2">{min}</p>
                  </div>
                </div>
              </Col>
              <Col>
                <div className="row d-flex justify-content-center">
                  <div className="flex-grow-1 justify-content-center">
                    <h3 className="mb-2">Max</h3>
                    <p className="mb-2">{max}</p>
                  </div>
                </div>
              </Col>
              <Col>
                <div className="row d-flex justify-content-center">
                  <div className="flex-grow-1 justify-content-center">
                    <h3 className="mb-2">Avg</h3>
                    <p className="mb-2">{avg}</p>
                  </div>
                </div>
              </Col>
            </Row>
            <Row>
              <Col>
                <div className="row d-flex justify-content-center">
                  <div className="flex-grow-1 justify-content-center">
                    <h3 className="mb-2">K</h3>
                    <p className="mb-2">{kills}</p>
                  </div>
                </div>
              </Col>
              <Col>
                <div className="row d-flex justify-content-center">
                  <div className="flex-grow-1 justify-content-center">
                    <h3 className="mb-2">A</h3>
                    <p className="mb-2">{assists}</p>
                  </div>
                </div>
              </Col>
              <Col>
                <div className="row d-flex justify-content-center">
                  <div className="flex-grow-1 justify-content-center">
                    <h3 className="mb-2">D</h3>
                    <p className="mb-2">{deaths}</p>
                  </div>
                </div>
              </Col>
            </Row>
            <Row>
              <Col>
                <div className="row d-flex justify-content-center">
                  <div className="flex-grow-1 justify-content-center">
                    <h3 className="mb-2">Dmg</h3>
                    <p className="mb-2">{damage}</p>
                  </div>
                </div>
              </Col>
              <Col>
                <div className="row d-flex justify-content-center">
                  <div className="flex-grow-1 justify-content-center">
                    <h3 className="mb-2">DmgRec</h3>
                    <p className="mb-2">{damageReceived}</p>
                  </div>
                </div>
              </Col>
            </Row>
            <Row>
              <Col>
                <div className="row d-flex justify-content-center">
                  <div className="flex-grow-1 justify-content-center">
                    <h3 className="mb-2">MVP</h3>
                    <p className="mb-2">{mvp}</p>
                  </div>
                </div>
              </Col>
              <Col>
                <div className="row d-flex justify-content-center">
                  <div className="flex-grow-1 justify-content-center">
                    <h3 className="mb-2">Score</h3>
                    <p className="mb-2">{score}</p>
                  </div>
                </div>
              </Col>
              <Col>
                <div className="row d-flex justify-content-center">
                  <div className="flex-grow-1 justify-content-center">
                    <h3 className="mb-2">Time</h3>
                    <p className="mb-2">{time}</p>
                  </div>
                </div>
              </Col>
            </Row>
          </Container>
        </Card.Body>
      </Card>
    </Col>
  );
};

export default MinMaxAvg;
